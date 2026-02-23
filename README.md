# Macro Economic Data Analyzer

A Python script for processing CSV files with macroeconomic data and generating reports.

## Features

- Read and combine data from multiple CSV files
- Generate average GDP reports by country
- Extensible architecture for adding new report types
- Clean tabular output using the `tabulate` library
- Comprehensive test coverage

## Installation

### Option 1: Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd MacroEconomyCsv
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Docker Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd MacroEconomyCsv
```

2. Build the Docker image:
```bash
docker build -t macro-analyzer .
```

3. Or use Docker Compose:
```bash
docker-compose build
```

## Usage

### Local Usage

Generate average GDP report from one or more CSV files:

```bash
python macro_analyzer.py --files economic1.csv economic2.csv --report average-gdp
```

### Docker Usage

#### Using Docker Run

1. Run with built-in sample data:
```bash
docker run --rm macro-analyzer python macro_analyzer.py --files economic1.csv economic2.csv --report average-gdp
```

2. Run with custom data (mount volume):
```bash
docker run --rm -v /path/to/your/data:/app/data macro-analyzer python macro_analyzer.py --files /app/data/your_file.csv --report average-gdp
```

3. Show help:
```bash
docker run --rm macro-analyzer --help
```

#### Using Docker Compose

1. Run with sample data:
```bash
docker-compose --profile sample up
```

2. Run custom analysis:
```bash
docker-compose run --rm macro-analyzer python macro_analyzer.py --files economic1.csv economic2.csv --report average-gdp
```

3. Show help:
```bash
docker-compose run --rm macro-analyzer python macro_analyzer.py --help
```

### Command Line Arguments

- `--files`: One or more CSV files with economic data (required)
- `--report`: Type of report to generate (required, currently only `average-gdp` is available)

### Example Output

```
+----------------+--------------+
| Country        |   Average GDP |
+================+==============+
| United States  |     23923.67 |
+----------------+--------------+
| China          |     17810.33 |
+----------------+--------------+
| Germany        |      4138.33 |
+----------------+--------------+
| Japan          |      4467.00 |
+----------------+--------------+
| India          |      3423.67 |
+----------------+--------------+
```

## CSV File Format

The CSV files should have the following columns:

```
country,year,gdp,gdp_growth,inflation,unemployment,population,continent
United States,2023,25462,2.1,3.4,3.7,339,North America
United States,2022,23315,2.1,8.0,3.6,338,North America
```

## Running Tests

Run the test suite using pytest:

```bash
pytest test_macro_analyzer.py -v
```

## Architecture

The script is designed with extensibility in mind:

- **Report Registry**: New report types can be added by creating functions and registering them in the `REPORTS` dictionary
- **Modular Design**: Separate functions for reading data, processing, and generating reports
- **Type Hints**: Full type annotation support for better code maintainability

### Adding New Reports

To add a new report type:

1. Create a function that takes `List[Dict[str, Any]]` data and returns `List[Dict[str, Any]]`
2. Register the function in the `REPORTS` dictionary
3. Add the report name to the argument parser choices

Example:
```python
def calculate_population_by_continent(data):
    # Your implementation here
    return result

REPORTS['population-by-continent'] = calculate_population_by_continent
```

## Dependencies

- `tabulate`: For formatted table output
- `pytest`: For testing (development dependency)

## Docker Requirements

- Docker 20.10 or higher
- Docker Compose 1.29 or higher (for compose usage)

## Python Version

Requires Python 3.7 or higher (Docker image uses Python 3.13).

## License

This project is open source and available under the MIT License.
