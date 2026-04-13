import os

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")

def _resolve(path: str) -> str:
    """Eger tam yol verilmemisse Desktop'a kaydet."""
    if not os.path.isabs(path):
        return os.path.join(DESKTOP, path)
    return path

def file_write(path: str, content: str) -> str:
    """Dosyaya yazar (yoksa olusturur, varsa uzerine yazar)."""
    full = _resolve(path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Dosya yazildi: {full}"

def file_append(path: str, content: str) -> str:
    """Dosyanin sonuna ekler."""
    full = _resolve(path)
    with open(full, "a", encoding="utf-8") as f:
        f.write(content + "\n")
    return f"Eklendi: {full}"

def file_read(path: str) -> str:
    """Dosyayi okur ve icerigini dondurur."""
    full = _resolve(path)
    if not os.path.exists(full):
        return f"Dosya bulunamadi: {full}"
    with open(full, "r", encoding="utf-8") as f:
        return f.read()

def file_delete(path: str) -> str:
    """Dosyayi siler."""
    full = _resolve(path)
    if not os.path.exists(full):
        return f"Dosya bulunamadi: {full}"
    os.remove(full)
    return f"Dosya silindi: {full}"

def file_list(path: str = ".") -> str:
    """Klasordeki dosyalari listeler."""
    full = _resolve(path)
    if not os.path.exists(full):
        return f"Klasor bulunamadi: {full}"
    items = os.listdir(full)
    return "\n".join(items) if items else "Klasor bos."
