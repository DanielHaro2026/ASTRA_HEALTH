from pathlib import Path

extensions = {
    ".html", ".py", ".css", ".js", ".json",
    ".txt", ".md", ".xml", ".yml", ".yaml"
}

excluded = {
    ".git", ".venv", "venv", "__pycache__",
    "node_modules", "instance"
}

patterns = [
    "Ã", "Â", "â€", "âœ", "ðŸ",
    "ï»¿", "�"
]

found = 0

for file in Path(".").rglob("*"):
    if not file.is_file():
        continue

    if file.suffix.lower() not in extensions:
        continue

    if any(part in excluded for part in file.parts):
        continue

    try:
        content = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"\nERROR UTF-8: {file}")
        found += 1
        continue

    for number, line in enumerate(content.splitlines(), 1):
        if any(pattern in line for pattern in patterns):
            print(f"\nARCHIVO: {file} | LINEA: {number}")
            print(line.strip())
            found += 1

print(f"\nTOTAL DE DETECCIONES: {found}")
