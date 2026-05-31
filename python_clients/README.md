
Перед запуском нужно установить недостающие либы:

```
python -m pip install -r requirements.txt
```

Для запуска получения данных через запуск утилиты командной строки нужно выполнить:
```
python scrape_ozon_cli.py parameters.json
```
Файл parameters.json берется из подпапки results, если у файла не указаны абсолютные пути.
И в этот же каталог сохраняется результат.

Для запуска GUI утилиты нужно выполнить
```
python scrape_ozon_gui.py
```

Графический интерфейс позволяет получать данные без ввода команд, а просто нажатием кнопок.<br>
Результат может быть в виде JSON или CSV.<br>
Результат можно сохранить в файл или скопировать в буфер обмена.<br>

<img width="495" height="364" alt="2026-06-01_01-19" src="https://github.com/user-attachments/assets/9238095e-b79b-4f5b-9cde-9c1baa57328c" />
<br><br>
И результат:<br><br>
<img width="490" height="358" alt="2026-06-01_01-18" src="https://github.com/user-attachments/assets/e51c0f31-3e42-47ab-9207-37ac5adec2cc" />
