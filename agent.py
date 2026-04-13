import time
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, JARVIS_SYSTEM_PROMPT, MAX_HISTORY
from tools.browser_tool import browser_search, browser_open
from tools.browser_control_tool import youtube_play_song, youtube_music_play_song, browser_play_pause, browser_next_track
from tools.file_tool import file_write, file_append, file_read, file_delete, file_list
from tools.app_tool import app_open, app_close
from tools.system_tool import volume_up, volume_down, volume_mute

TOOLS = [
    {
        "name": "browser_search",
        "description": "Google'da arama yapar.",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
    },
    {
        "name": "browser_open",
        "description": "URL'yi tarayicide acar.",
        "input_schema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}
    },
    {
        "name": "youtube_play_song",
        "description": "YouTube'da sarki/video arar ve otomatik olarak oynatir. Muzik isteklerinde kullan.",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string", "description": "Sarki ve sanatci adi"}}, "required": ["query"]}
    },
    {
        "name": "youtube_music_play_song",
        "description": "YouTube Music'te sarki arar ve otomatik oynatir.",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
    },
    {
        "name": "browser_play_pause",
        "description": "Tarayicidaki muzigi play veya pause yapar.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "browser_next_track",
        "description": "Sonraki sarkiya gecer.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "file_write",
        "description": "Dosya olusturur ve icerik yazar.",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}
    },
    {
        "name": "file_append",
        "description": "Var olan dosyaya ekleme yapar.",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}
    },
    {
        "name": "file_read",
        "description": "Dosya icerigini okur.",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}
    },
    {
        "name": "file_delete",
        "description": "Dosyayi siler.",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}
    },
    {
        "name": "file_list",
        "description": "Klasordeki dosyalari listeler.",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": []}
    },
    {
        "name": "app_open",
        "description": "Uygulama acar: spotify, chrome, notepad, calculator, vscode",
        "input_schema": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}
    },
    {
        "name": "app_close",
        "description": "Uygulamayi kapatir.",
        "input_schema": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}
    },
    {
        "name": "volume_up",
        "description": "Sesi arttirir.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "volume_down",
        "description": "Sesi azaltir.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "volume_mute",
        "description": "Sesi kapatir veya acar.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    },
]

def run_tool(name, inputs):
    mapping = {
        "browser_search":          lambda i: browser_search(i["query"]),
        "browser_open":            lambda i: browser_open(i["url"]),
        "youtube_play_song":       lambda i: youtube_play_song(i["query"]),
        "youtube_music_play_song": lambda i: youtube_music_play_song(i["query"]),
        "browser_play_pause":      lambda i: browser_play_pause(),
        "browser_next_track":      lambda i: browser_next_track(),
        "file_write":              lambda i: file_write(i["path"], i["content"]),
        "file_append":             lambda i: file_append(i["path"], i["content"]),
        "file_read":               lambda i: file_read(i["path"]),
        "file_delete":             lambda i: file_delete(i["path"]),
        "file_list":               lambda i: file_list(i.get("path", ".")),
        "app_open":                lambda i: app_open(i["app_name"]),
        "app_close":               lambda i: app_close(i["app_name"]),
        "volume_up":               lambda i: volume_up(),
        "volume_down":             lambda i: volume_down(),
        "volume_mute":             lambda i: volume_mute(),
    }
    fn = mapping.get(name)
    if fn:
        try:
            return fn(inputs)
        except Exception as e:
            return f"Hata ({name}): {str(e)}"
    return f"Bilinmeyen tool: {name}"

def run_agent(user_input, history, retries=3):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    history.append({"role": "user", "content": user_input})
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    for attempt in range(retries):
        try:
            while True:
                response = client.messages.create(
                    model=CLAUDE_MODEL,
                    max_tokens=1024,
                    system=JARVIS_SYSTEM_PROMPT,
                    tools=TOOLS,
                    messages=history
                )
                if response.stop_reason == "tool_use":
                    assistant_content = response.content
                    history.append({"role": "assistant", "content": assistant_content})
                    tool_results = []
                    for block in assistant_content:
                        if block.type == "tool_use":
                            print(f"[Tool: {block.name} | {block.input}]")
                            result = run_tool(block.name, block.input)
                            print(f"[Sonuc: {result}]")
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result
                            })
                    history.append({"role": "user", "content": tool_results})
                else:
                    reply = response.content[0].text
                    history.append({"role": "assistant", "content": reply})
                    print(f"Jarvis: {reply}")
                    return reply, history

        except anthropic.APIStatusError as e:
            if e.status_code == 529 and attempt < retries - 1:
                wait = (attempt + 1) * 3
                print(f"Sunucu yogun, {wait}s bekliyorum...")
                time.sleep(wait)
            else:
                raise

    return "Hata.", history
