# Анализатор макроэкономических данных

Python-скрипт для обработки CSV-файлов с макроэкономическими данными и генерации отчетов.

## Возможности

- Чтение и объединение данных из нескольких CSV-файлов
- Генерация отчетов о среднем ВВП по странам
- Расширяемая архитектура для добавления новых типов отчетов
- Форматированный вывод в виде таблиц с использованием библиотеки `tabulate`
- Комплексное тестовое покрытие

## Установка

### Способ 1: Локальная установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd MacroEconomyCsv
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

### Способ 2: Установка через Docker

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd MacroEconomyCsv
```

2. Соберите Docker-образ:
```bash
docker build -t macro-analyzer .
```

3. Или используйте Docker Compose:
```bash
docker-compose build
```

## Использование

### Локальный запуск

Генерация отчета о среднем ВВП из одного или нескольких CSV-файлов:

```bash
python macro_analyzer.py --files economic1.csv economic2.csv --report average-gdp
```

### Использование Docker

#### Через Docker Run

1. Запуск со встроенными примерами данных:
```bash
docker run --rm macro-analyzer python macro_analyzer.py --files economic1.csv economic2.csv --report average-gdp
```

2. Запуск с кастомными данными (монтирование тома):
```bash
docker run --rm -v /path/to/your/data:/app/data macro-analyzer python macro_analyzer.py --files /app/data/your_file.csv --report average-gdp
```

3. Показать справку:
```bash
docker run --rm macro-analyzer --help
```

#### Через Docker Compose

1. Запуск с примерами данных:
```bash
docker-compose --profile sample up
```

2. Запуск кастомного анализа:
```bash
docker-compose run --rm macro-analyzer python macro_analyzer.py --files economic1.csv economic2.csv --report average-gdp
```

3. Показать справку:
```bash
docker-compose run --rm macro-analyzer python macro_analyzer.py --help
```

### Аргументы командной строки

- `--files`: Один или несколько CSV-файлов с экономическими данными (обязательно)
- `--report`: Тип отчета для генерации (обязательно, сейчас доступен только `average-gdp`)

### Пример вывода

```
+----------------+---------------+
| Country        |   Average GDP |
+================+===============+
| United States  |      23923.7  |
+----------------+---------------+
| China          |      17810.3  |
+----------------+---------------+
| Germany        |       4138.33 |
+----------------+---------------+
| Japan          |       4467.00 |
+----------------+---------------+
| India          |       3423.67 |
+----------------+---------------+
```

## Формат CSV-файлов

CSV-файлы должны содержать следующие столбцы:

```
country,year,gdp,gdp_growth,inflation,unemployment,population,continent
United States,2023,25462,2.1,3.4,3.7,339,North America
United States,2022,23315,2.1,8.0,3.6,338,North America
```

## Запуск тестов

Запустите тестовый набор с помощью pytest:

```bash
pytest test_macro_analyzer.py -v
```

## Архитектура

Скрипт разработан с учетом расширяемости:

- **Реестр отчетов**: Новые типы отчетов можно добавлять, создавая функции и регистрируя их в словаре `REPORTS`
- **Модульный дизайн**: Отдельные функции для чтения данных, обработки и генерации отчетов
- **Типизация**: Полная поддержка аннотаций типов для лучшей поддерживаемости кода

### Добавление новых отчетов

Для добавления нового типа отчета:

1. Создайте функцию, которая принимает `List[Dict[str, Any]]` данные и возвращает `List[Dict[str, Any]]`
2. Зарегистрируйте функцию в словаре `REPORTS`
3. Добавьте имя отчета в choices парсера аргументов

Пример:
```python
def calculate_population_by_continent(data):
    # Ваша реализация здесь
    return result

REPORTS['population-by-continent'] = calculate_population_by_continent
```

## Зависимости

- `tabulate`: Для форматированного вывода таблиц
- `pytest`: Для тестирования (зависимость для разработки)

## Требования к Docker

- Docker 20.10 или выше
- Docker Compose 1.29 или выше (для использования compose)

## Версия Python

Требуется Python 3.7 или выше (Docker-образ использует Python 3.13).

## Makefile

Для удобства разработки предоставлен Makefile с основными командами:

```bash
# Локальная разработка
make install    # Установить зависимости
make test       # Запустить тесты
make run        # Запустить анализ с примерами
make demo       # Запустить демонстрацию

# Docker команды
make docker-build    # Собрать Docker-образ
make docker-run      # Запустить Docker-контейнер
make docker-test     # Протестировать Docker-функциональность
make docker-clean    # Очистить Docker-ресурсы
```

## Лицензия

Этот проект является открытым исходным кодом и доступен под лицензией MIT.
