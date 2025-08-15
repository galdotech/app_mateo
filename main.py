# -*- coding: utf-8 -*-
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QApplication, QDialog

from app.views.main_window import MainWindow
from app.views.login_dialog import LoginDialog
from app.data import db


def load_stylesheet(path: Path) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception as err:
        print(err)
        return ""


def main():
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(db.close_db)

    settings = QSettings("galdotech", "app_mateo")
    theme = settings.value("ui/theme", "light")
    qss_path = Path(__file__).resolve().parent / "app" / "resources" / f"theme_{theme}.qss"
    app.setStyleSheet(load_stylesheet(qss_path))

    # Inicializa BD (lazy-safe: crea si no existe)
    db.init_db()

    login = LoginDialog()
    if login.exec() != QDialog.Accepted:
        sys.exit(0)

    win = MainWindow(settings, login.user_role or "")
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
