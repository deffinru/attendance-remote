"""Модуль учёта посещений."""
import csv
from datetime import date, datetime

# Порог опоздания в минутах
LATE_MINUTES = 0

def check_in(name: str, filename: str = "attendance.csv") -> None:
    """Зарегистрировать вход сотрудника."""
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, "in", datetime.now().isoformat()])

def check_out(name: str, filename: str = "attendance.csv") -> None:
    """Зарегистрировать выход сотрудника."""
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, "out", datetime.now().isoformat()])

def calculate_duration(name: str, filename: str = "attendance.csv") -> float:
    """Рассчитать длительность последнего сеанса (в часах)."""
    in_time = None
    out_time = None
    with open(filename, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3 or row[0] != name:
                continue
            if row[1] == "in":
                in_time = datetime.fromisoformat(row[2])
            elif row[1] == "out":
                out_time = datetime.fromisoformat(row[2])

    if in_time is None or out_time is None:
        return 0.0
    return (out_time - in_time).total_seconds() / 3600

def mark_late(
    name: str,
    deadline: str,
    filename: str = "attendance.csv",
    current: str | None = None,
) -> None:
    """Отметить вход с учётом опоздания (с допуском LATE_MINUTES)."""
    from datetime import timedelta

    now = current or datetime.now().strftime("%H:%M")
    deadline_t = datetime.strptime(deadline, "%H:%M")
    
    # Добавляем допуск LATE_MINUTES к дедлайну
    deadline_with_tolerance = (deadline_t + timedelta(minutes=LATE_MINUTES)).time()
    now_t = datetime.strptime(now, "%H:%M").time()

    event = "late" if now_t > deadline_with_tolerance else "in"

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, event, datetime.now().isoformat()])


if __name__ == "__main__":
    name = input("Введите имя: ")
    check_in(name)
    print("Вход зарегистрирован.")