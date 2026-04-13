import webbrowser
import urllib.parse

def browser_search(query: str) -> str:
    """Google'da arama yapar."""
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"Arama yapildi: {query}"

def browser_open(url: str) -> str:
    """URL'yi tarayicide acar."""
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Acildi: {url}"

def youtube_play(query: str) -> str:
    """YouTube'da sarki/video arar ve ilk sonucu otomatik oynatir."""
    # YouTube arama sonuclarinda autoplay ile ilk videoyu ac
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    # Direkt arama sonucunu ac, kullanici ilk videoya tiklar
    webbrowser.open(url)
    return f"YouTube'da acildi: {query}"

def youtube_music_play(query: str) -> str:
    """YouTube Music'te sarki calar."""
    url = f"https://music.youtube.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"YouTube Music'te acildi: {query}"

def spotify_search(query: str) -> str:
    """Spotify web'de sarki acar."""
    url = f"https://open.spotify.com/search/{urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"Spotify'da acildi: {query}"
