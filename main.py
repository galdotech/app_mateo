# -*- coding: utf-8 -*-
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.views.main_window import MainWindow
from app.data import db

def main():
    app = QApplication(sys.argv)

    # Cargar tema QSS si está disponible
    qss_path = Path(__file__).resolve().parent / "app" / "resources" / "theme.qss"
    if qss_path.exists():
        try:
            with open(qss_path, "r", encoding="utf-8") as fh:
                app.setStyleSheet(fh.read())
        except Exception:
            # Ignora errores de lectura del tema
            pass

    # Inicializa BD (lazy-safe: crea si no existe)
    db.init_db()

    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
