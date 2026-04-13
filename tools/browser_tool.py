import webbrowser
import urllib.parse

def browser_search(query: str) -> str:
    """Web'de arama yapar ve tarayiciyi acar."""
    encoded = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded}"
    webbrowser.open(url)
    return f"'{query}' icin Google'da arama yapildi ve tarayici acildi."

def browser_open(url: str) -> str:
    """Verilen URL'yi tarayicide acar."""
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"{url} tarayicide acildi."
