from pathlib import Path

ROOT = Path(".")
EXTENSIONS = {".html", ".py", ".css", ".js"}
EXCLUDE = {".git", ".venv", "venv", "__pycache__"}

replacements = {
    "✨": "✨",
    "✔": "✔",
    "–": "–",
    "—": "—",
    "’": "’",
    "“": "“",
    "”": "”",
}

modified = 0

for file in ROOT.rglob("*"):
    if not file.is_file():
        continue

    if any(part in EXCLUDE for part in file.parts):
        continue

    if file.suffix.lower() not in EXTENSIONS:
        continue

    try:
        content = file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue

    original = content

    for wrong, correct in replacements.items():
        content = content.replace(wrong, correct)

    if file.suffix.lower() == ".html":
        if "<head" in content.lower() and "charset" not in content.lower():
            import re
            content = re.sub(
                r"(<head[^>]*>)",
                r'\1\n    <meta charset="UTF-8">',
                content,
                count=1,
                flags=re.IGNORECASE
            )

    if content != original:
        file.write_text(content, encoding="utf-8")
        print(f"CORREGIDO: {file}")
        modified += 1

print(f"\nProceso terminado. Archivos modificados: {modified}")
