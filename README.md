# Inventario Base (PySide6 + SQLite)

Proyecto base mínimo con estructura MVC para app de escritorio en Linux (PySide6 + SQLite).

## Requisitos
- Python 3.10+ recomendado
- Linux (funciona también en macOS/Windows)
- `pip install -r requirements.txt`

## Entorno
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Tema e iconos
Los recursos de estilo e iconografía se recompilan con:
```bash
pyside6-rcc app/resources/icons.qrc -o app/resources/icons_rc.py
pyside6-uic app/ui/<archivo>.ui -o app/ui/ui_<archivo>.py
```
