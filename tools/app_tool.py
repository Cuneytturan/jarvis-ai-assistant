import subprocess
import os

APPS = {
    "spotify": r"C:\Users\User\AppData\Roaming\Spotify\Spotify.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "explorer": "explorer.exe",
    "vscode": r"C:\Users\User\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
}

def app_open(app_name: str) -> str:
    """Uygulamayi acar."""
    name = app_name.lower().strip()
    if name in APPS:
        path = APPS[name]
        try:
            subprocess.Popen(path)
            return f"{app_name} acildi."
        except Exception as e:
            return f"{app_name} acilamadi: {str(e)}"
    else:
        # Dogrudan calistirmayi dene
        try:
            subprocess.Popen(app_name)
            return f"{app_name} acildi."
        except Exception:
            available = ", ".join(APPS.keys())
            return f"Uygulama bulunamadi. Bilinen uygulamalar: {available}"

def app_close(app_name: str) -> str:
    """Uygulamayi kapatir (Windows)."""
    try:
        os.system(f"taskkill /f /im {app_name}.exe")
        return f"{app_name} kapatildi."
    except Exception as e:
        return f"Kapatma hatasi: {str(e)}"
