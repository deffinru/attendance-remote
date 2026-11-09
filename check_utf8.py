import os
import sys

def main():
    for root, dirs, files in os.walk("."):
        # Пропускаем скрытые папки (например, .git)
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        
        for file in files:
            # Проверяем только текстовые расширения
            if file.endswith((".py", ".md", ".csv", ".example", ".txt", ".json")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        f.read()
                except UnicodeDecodeError:
                    print(f"ОШИБКА: Файл {filepath} не является корректным UTF-8")
                    sys.exit(1)
    print("Все текстовые файлы успешно прочитаны в кодировке UTF-8.")

if __name__ == "__main__":
    main()