# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog, QVBoxLayout, QCalendarWidget, QListWidget
from PySide6.QtCore import QDate

from app.data import db


class CalendarDialog(QDialog):
    """Simple calendar view for scheduled repairs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calendario de tareas")
        layout = QVBoxLayout(self)
        self.calendar = QCalendarWidget(self)
        self.tasks = QListWidget(self)
        layout.addWidget(self.calendar)
        layout.addWidget(self.tasks)
        self.calendar.selectionChanged.connect(self._load_tasks)
        self._load_tasks()

    def _load_tasks(self) -> None:
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.tasks.clear()
        for _id, desc, tech in db.get_tasks_by_date(date):
            if tech:
                self.tasks.addItem(f"{desc} ({tech})")
            else:
                self.tasks.addItem(desc)
