import time
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, JARVIS_SYSTEM_PROMPT, MAX_HISTORY
from tools.browser_tool import browser_search, browser_open
from tools.file_tool import file_write, file_append, file_read, file_delete, file_list
from tools.app_tool import app_open, app_close
from tools.system_tool import set_volume, volume_up, volume_down, volume_mute

# --- Tool tanimlari (Claude'a ne yapabilecegini anlat) ---
TOOLS = [
    {
        "name": "browser_search",
        "description": "Google'da web aramasi yapar ve tarayiciyi acar.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Aranacak terim"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "browser_open",
        "description": "Belirtilen URL'yi tarayicide acar.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Acilacak URL"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "file_write",
        "description": "Bir dosyaya icerik yazar. Kod yazma, not alma, liste olusturma icin kullan.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Dosya adi veya tam yolu"},
                "content": {"type": "string", "description": "Yazilacak icerik"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "file_append",
        "description": "Mevcut bir dosyanin sonuna icerik ekler.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Dosya adi veya tam yolu"},
                "content": {"type": "string", "description": "Eklenecek icerik"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "file_read",
        "description": "Bir dosyanin icerigini okur.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Dosya adi veya tam yolu"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "file_delete",
        "description": "Bir dosyayi siler.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Silinecek dosya adi"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "file_list",
        "description": "Bir klasordeki dosyalari listeler.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Klasor yolu (varsayilan: Desktop)"}
            },
            "required": []
        }
    },
    {
        "name": "app_open",
        "description": "Bir uygulamayi acar. Ornek: spotify, chrome, notepad, calculator, vscode",
        "input_schema": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Uygulama adi"}
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "app_close",
        "description": "Bir uygulamayi kapatir.",
        "input_schema": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Kapatilacak uygulama adi"}
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "volume_up",
        "description": "Sistem sesini arttirir.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "volume_down",
        "description": "Sistem sesini azaltir.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "volume_mute",
        "description": "Sistemi sessize alir veya sesi acar.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
]

# --- Tool calistirici ---
def run_tool(name: str, inputs: dict) -> str:
    mapping = {
        "browser_search": lambda i: browser_search(i["query"]),
        "browser_open":   lambda i: browser_open(i["url"]),
        "file_write":     lambda i: file_write(i["path"], i["content"]),
        "file_append":    lambda i: file_append(i["path"], i["content"]),
        "file_read":      lambda i: file_read(i["path"]),
        "file_delete":    lambda i: file_delete(i["path"]),
        "file_list":      lambda i: file_list(i.get("path", ".")),
        "app_open":       lambda i: app_open(i["app_name"]),
        "app_close":      lambda i: app_close(i["app_name"]),
        "volume_up":      lambda i: volume_up(),
        "volume_down":    lambda i: volume_down(),
        "volume_mute":    lambda i: volume_mute(),
    }
    fn = mapping.get(name)
    if fn:
        try:
            return fn(inputs)
        except Exception as e:
            return f"Tool hatasi ({name}): {str(e)}"
    return f"Bilinmeyen tool: {name}"

# --- Ana agent dongusu ---
def run_agent(user_input: str, history: list, retries: int = 3) -> tuple:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    history.append({"role": "user", "content": user_input})
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    for attempt in range(retries):
        try:
            # Agent dongusu: Claude araclari kullanana kadar doner
            while True:
                response = client.messages.create(
                    model=CLAUDE_MODEL,
                    max_tokens=2048,
                    system=JARVIS_SYSTEM_PROMPT,
                    tools=TOOLS,
                    messages=history
                )

                # Tool kullanimi var mi?
                if response.stop_reason == "tool_use":
                    # Tum content'i history'e ekle
                    assistant_content = response.content
                    history.append({"role": "assistant", "content": assistant_content})

                    # Tool'lari calistir
                    tool_results = []
                    for block in assistant_content:
                        if block.type == "tool_use":
                            print(f"[Jarvis tool kullaniyor: {block.name}({block.input})]")
                            result = run_tool(block.name, block.input)
                            print(f"[Sonuc: {result}]")
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result
                            })

                    # Tool sonuclarini history'e ekle
                    history.append({"role": "user", "content": tool_results})

                else:
                    # Son cevap hazir
                    reply = response.content[0].text
                    history.append({"role": "assistant", "content": reply})
                    print(f"Jarvis: {reply}")
                    return reply, history

        except anthropic.APIStatusError as e:
            if e.status_code == 529 and attempt < retries - 1:
                wait = (attempt + 1) * 3
                print(f"Sunucu yogun, {wait} saniye bekliyorum...")
                time.sleep(wait)
            else:
                raise

    return "Uzgunum, su an cevap veremiyorum.", history
