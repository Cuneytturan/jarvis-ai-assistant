import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

_driver = None

def get_driver():
    """Paylasilan Chrome driver - bir kez ac, hep kullan."""
    global _driver
    if _driver is None:
        options = Options()
        options.add_argument("--start-maximized")
        # Mevcut Chrome profilini kullan (YouTube Music giris bilgileri icin)
        import os
        profile = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data")
        options.add_argument(f"--user-data-dir={profile}")
        options.add_argument("--profile-directory=Default")
        service = Service(ChromeDriverManager().install())
        _driver = webdriver.Chrome(service=service, options=options)
    return _driver

def youtube_music_play_song(query: str) -> str:
    """YouTube Music'te sarki arar ve ilk sonucu otomatik oynatir."""
    driver = get_driver()
    try:
        url = f"https://music.youtube.com/search?q={urllib.parse.quote(query)}"
        driver.get(url)
        time.sleep(3)
        # İlk sarki sonucuna tikla
        selectors = [
            "ytmusic-shelf-renderer ytmusic-responsive-list-item-renderer",
            "ytmusic-card-shelf-renderer",
            "#contents ytmusic-responsive-list-item-renderer"
        ]
        for sel in selectors:
            try:
                items = driver.find_elements(By.CSS_SELECTOR, sel)
                if items:
                    items[0].click()
                    time.sleep(2)
                    return f"Oynatiluyor: {query}"
            except:
                continue
        return f"YouTube Music'te acildi: {query}"
    except Exception as e:
        return f"Hata: {str(e)}"

def youtube_play_song(query: str) -> str:
    """YouTube'da sarki arar ve ilk video sonucunu oynatir."""
    driver = get_driver()
    try:
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        driver.get(url)
        time.sleep(3)
        # İlk video sonucuna tikla
        videos = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer #video-title")
        if videos:
            videos[0].click()
            time.sleep(2)
            return f"Oynatiluyor: {query}"
        return f"Sonuc bulunamadi: {query}"
    except Exception as e:
        return f"Hata: {str(e)}"

def browser_play_pause() -> str:
    """Aktif tarayici sekmesinde play/pause yapar."""
    driver = get_driver()
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)
        return "Play/Pause yapildi."
    except Exception as e:
        return f"Hata: {str(e)}"

def browser_next_track() -> str:
    """Sonraki parkaya gecer."""
    driver = get_driver()
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_RIGHT)
        return "Sonraki parka gecildi."
    except Exception as e:
        return f"Hata: {str(e)}"
