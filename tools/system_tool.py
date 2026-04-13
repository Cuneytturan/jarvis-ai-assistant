import subprocess

def set_volume(level: int) -> str:
    """Ses seviyesini ayarlar (0-100)."""
    level = max(0, min(100, level))
    script = f"(New-Object -com Shell.Application).Windows() | Out-Null; $obj = New-Object -ComObject WScript.Shell; $obj.SendKeys([char]174*5)"
    # PowerShell ile ses ayarla
    ps = f"""
$vol = {level}
$wshShell = New-Object -ComObject WScript.Shell
[audio]::Volume = $vol / 100
"""
    try:
        subprocess.run(["powershell", "-c",
            f"$vol={level}/100; (New-Object -ComObject WScript.Shell); Add-Type -TypeDefinition 'using System.Runtime.InteropServices; public class Audio {{ [DllImport(\"winmm.dll\")] public static extern int waveOutSetVolume(int h, uint v); }}'; [Audio]::waveOutSetVolume(0, [uint32](($vol)*0xFFFF + ($vol)*0xFFFF*0x10000))"],
            capture_output=True)
        return f"Ses seviyesi {level} yapildi."
    except Exception as e:
        return f"Ses ayarlanamadi: {str(e)}"

def volume_up() -> str:
    """Sesi arttirir."""
    try:
        subprocess.run(["powershell", "-c",
            "(New-Object -com Shell.Application); $wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]175)"],
            capture_output=True)
        return "Ses arttirildi."
    except Exception as e:
        return f"Hata: {str(e)}"

def volume_down() -> str:
    """Sesi azaltir."""
    try:
        subprocess.run(["powershell", "-c",
            "$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]174)"],
            capture_output=True)
        return "Ses azaltildi."
    except Exception as e:
        return f"Hata: {str(e)}"

def volume_mute() -> str:
    """Sesi kapatir/acar."""
    try:
        subprocess.run(["powershell", "-c",
            "$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]173)"],
            capture_output=True)
        return "Ses kapatildi/acildi."
    except Exception as e:
        return f"Hata: {str(e)}"

def get_volume() -> str:
    """Mevcut ses seviyesini dondurur."""
    try:
        result = subprocess.run(["powershell", "-c",
            "[math]::Round((Get-WmiObject Win32_SoundDevice | Select -First 1).StatusInfo)"],
            capture_output=True, text=True)
        return f"Ses seviyesi: {result.stdout.strip()}"
    except Exception as e:
        return f"Hata: {str(e)}"
