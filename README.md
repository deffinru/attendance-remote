# Attendance — учёт посещений

Простой Python-скрипт для учёта посещений с сохранением в CSV.

## Использование

python attendance.py

## Формат данных

См. attendance.csv.example.

## Функции

### check_in(name, filename)

Регистрирует вход сотрудника. Записывает в CSV строку:

name,event,datetime

Пример:

python attendance.py

### check_out(name, filename)

Регистрирует выход сотрудника. Формат строки такой же, как у check_in, но событие = out.

### calculate_duration(name, filename)

Рассчитывает длительность последнего сеанса (в часах) между check_in и check_out.

### mark_late(name, deadline, filename, current)

Отмечает вход с учётом опоздания. Если время входа позже `deadline` —
в CSV пишется событие `late`, иначе `in`.

Пример:

```python
from attendance import mark_late

mark_late("Иван", "09:00")              # реальное время
mark_late("Иван", "09:00", current="09:45")  # принудительно 09:45