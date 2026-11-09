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
        
    def test_mark_late_exact_boundary(self):
        """Если опоздание ровно на LATE_MINUTES, это еще не late (строго больше)."""
        # Если LATE_MINUTES = 10, дедлайн 09:00, то в 09:10 - это еще "in"
        mark_late("Иван", "09:00", self.filename, current="09:10")
        with open(self.filename, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("in", content)  
        self.assertNotIn("late", content)
        
class TestAdditionalRequirements(unittest.TestCase):
    def setUp(self):
        self.filename = "test_attendance.csv"
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_file_created_on_check_in(self):
        """7-й тест: файл создается"""
        check_in("Тест", self.filename)
        self.assertTrue(os.path.exists(self.filename))

    def test_duration_zero_if_no_out(self):
        """8-й тест: если нет выхода, длительность 0"""
        check_in("Тест", self.filename)
        self.assertEqual(calculate_duration("Тест", self.filename), 0.0)

    def test_duration_positive(self):
        """9-й тест: длительность положительная"""
        check_in("Тест", self.filename)
        check_out("Тест", self.filename)
        self.assertGreaterEqual(calculate_duration("Тест", self.filename), 0.0)

    def test_mark_late_no_file_crash(self):
        """10-й тест: функция не падает при отсутствии файла"""
        try:
            mark_late("Тест", "09:00", "nonexistent.csv", current="10:00")
        except Exception as e:
            self.fail(f"mark_late вызвала исключение: {e}")

    def test_duration_crosses_midnight(self):
        """11-й тест (целевой для варианта 6): время выхода раньше входа"""
        check_in("Ночной", self.filename)
        
        # Вручную подменяем время выхода на более раннее
        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            import csv
            from datetime import datetime, timedelta
            writer = csv.writer(f)
            out_time = datetime.now() - timedelta(hours=1)
            writer.writerow(["Ночной", "out", out_time.isoformat()])
            
        duration = calculate_duration("Ночной", self.filename)
        
        # Проверяем, что она НЕ отрицательная
        self.assertGreaterEqual(duration, 0.0, "Длительность не может быть отрицательной!")


if __name__ == "__main__":
    unittest.main()