"""Тесты для модуля attendance."""
import os
import unittest

from attendance import check_in, check_out, calculate_duration, mark_late


class TestCheckIn(unittest.TestCase):
    def setUp(self):
        self.filename = "test_attendance.csv"
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_check_in_creates_record(self):
        """Проверяем, что check_in создаёт запись."""
        check_in("Иван", self.filename)
        self.assertTrue(os.path.exists(self.filename))


class TestCheckOut(unittest.TestCase):
    def setUp(self):
        self.filename = "test_attendance.csv"
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_check_out_creates_record(self):
        """Проверяем, что check_out создаёт запись."""
        check_in("Иван", self.filename)
        check_out("Иван", self.filename)
        with open(self.filename, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("out", content)


class TestCalculateDuration(unittest.TestCase):
    def setUp(self):
        self.filename = "test_attendance.csv"
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_duration_between_in_and_out(self):
        """Проверяем расчёт длительности между входом и выходом."""
        check_in("Иван", self.filename)
        check_out("Иван", self.filename)
        duration = calculate_duration("Иван", self.filename)
        self.assertIsInstance(duration, float)
        self.assertGreaterEqual(duration, 0)


class TestMarkLate(unittest.TestCase):
    def setUp(self):
        self.filename = "test_attendance.csv"
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_mark_late_before_deadline(self):
        """До дедлайна — обычный вход (in)."""
        mark_late("Иван", "09:00", self.filename, current="08:30")
        with open(self.filename, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("in", content)
        self.assertNotIn("late", content)

    def test_mark_late_after_deadline(self):
        """После дедлайна — отметка late."""
        mark_late("Иван", "09:00", self.filename, current="09:45")
        with open(self.filename, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("late", content)


if __name__ == "__main__":
    unittest.main()