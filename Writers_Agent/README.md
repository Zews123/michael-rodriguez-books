# Book Publishing Workspace

Эта директория предназначена для создания и управления книгами с использованием **Autonomous Publishing Agent**.

## Структура

```
/Users/zews/Book/
├── AGENT_PROMPT.md          # Основной промпт для агента создания книг
├── SKILL.md                 # Навыки конвертации в Draft2Digital
├── README.md                # Этот файл
│
└── [Book_Name]/             # Отдельная папка для каждой книги
    ├── source/              # Исходные материалы
    │   ├── transcript.txt   # Транскрипт источника
    │   └── OUTLINE.md       # План книги
    │
    ├── output/              # Готовые файлы
    │   ├── Part_*.md        # Части книги
    │   ├── Full_Book.md     # Полная рукопись
    │   ├── Final_Book.docx  # Финальный DOCX для публикации
    │   ├── Cover_*.png      # Обложки
    │   ├── Publishing_Package.txt
    │   ├── Platform_Assessment.txt
    │   └── Cover_Brief.txt
    │
    └── gen_*.py             # Вспомогательные скрипты (опционально)
```

## Как использовать

1. **Запустить агента** с промптом из `AGENT_PROMPT.md`
2. Передать видео URL и название книги
3. Агент автоматически создаст папку `[Book_Name]/` и сгенерирует всю структуру
4. Для конвертации в DOCX используется скилл из `SKILL.md`

## Существующие книги

- **Shadows of Power** — Jeffrey Epstein and the Architecture of Impunity (2026)

## Примечания

- Каждая книга изолирована в своей папке
- Не смешивайте файлы разных книг
- Корневая директория содержит только общие инструменты (AGENT_PROMPT, SKILL)
