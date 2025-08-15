# -*- coding: utf-8 -*-
"""Utilities to export database tables to CSV or Excel files."""
from __future__ import annotations

import csv
from typing import List, Tuple

from . import db


def _fetch_table(table: str) -> Tuple[List[str], List[Tuple]]:
    """Return column names and all rows for the given table."""
    conn = db._ensure_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    headers = [col[0] for col in cur.description]
    return headers, rows


def export_table_to_csv(table: str, filepath: str) -> None:
    """Export the given table to a CSV file."""
    headers, rows = _fetch_table(table)
    with open(filepath, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(rows)


def export_table_to_excel(table: str, filepath: str) -> None:
    """Export the given table to an Excel file using openpyxl."""
    headers, rows = _fetch_table(table)
    try:
        from openpyxl import Workbook
    except Exception as exc:  # pragma: no cover - defensive
        raise RuntimeError("openpyxl is required for Excel export") from exc
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    for row in rows:
        ws.append(row)
    wb.save(filepath)
