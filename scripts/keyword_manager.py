"""keywords.csv에서 다음 키워드를 선택하고 사용 완료 처리"""
import csv
import os
from datetime import date
import config


def get_next_keyword() -> tuple[str, str] | None:
    """미사용 키워드 중 첫 번째 반환 (keyword, category)"""
    rows = _read_all()
    for row in rows:
        if row["used"].strip().lower() == "false":
            return row["keyword"].strip(), row["category"].strip()
    return None


def mark_used(keyword: str) -> None:
    rows = _read_all()
    for row in rows:
        if row["keyword"].strip() == keyword:
            row["used"] = "true"
            row["used_date"] = date.today().isoformat()
            break
    _write_all(rows)


def _read_all() -> list[dict]:
    with open(config.KEYWORDS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_all(rows: list[dict]) -> None:
    fieldnames = ["keyword", "category", "used", "used_date"]
    with open(config.KEYWORDS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
