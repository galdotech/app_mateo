# -*- coding: utf-8 -*-
import sys
from PySide6.QtWidgets import QApplication
from app.views.main_window import MainWindow
from app.data import db

def main():
    app = QApplication(sys.argv)
    # Inicializa BD (lazy-safe: crea si no existe)
    db.init_db()
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
