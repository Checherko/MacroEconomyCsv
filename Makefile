# Makefile for Macro Economic Data Analyzer

.PHONY: help build run test clean docker-build docker-run docker-test

# Default target
help:
	@echo "Macro Economic Data Analyzer - Available Commands:"
	@echo ""
	@echo "Local Development:"
	@echo "  install     Install Python dependencies"
	@echo "  test        Run pytest tests"
	@echo "  run         Run sample analysis locally"
	@echo "  demo        Run demonstration script"
	@echo "  clean       Clean Python cache files"
	@echo ""
	@echo "Docker Commands:"
	@echo "  docker-build    Build Docker image"
	@echo "  docker-run      Run Docker container with sample data"
	@echo "  docker-test     Test Docker functionality"
	@echo "  docker-clean    Remove Docker images and containers"
	@echo ""
	@echo "Examples:"
	@echo "  make install"
	@echo "  make docker-build"
	@echo "  make docker-run"

# Local development commands
install:
	pip install -r requirements.txt

test:
	pytest test_macro_analyzer.py -v

run:
	python macro_analyzer.py --files economic1.csv economic2.csv --report average-gdp

demo:
	python demo.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf pytest-cache-files-*

# Docker commands
docker-build:
	docker build -t macro-analyzer .

docker-run:
	docker run --rm macro-analyzer python macro_analyzer.py --files economic1.csv economic2.csv --report average-gdp

docker-test:
	@echo "Building Docker image..."
	docker build -t macro-analyzer .
	@echo "Testing help command..."
	docker run --rm macro-analyzer --help
	@echo "Testing analysis with sample data..."
	docker run --rm macro-analyzer python macro_analyzer.py --files economic1.csv economic2.csv --report average-gdp

docker-compose-build:
	docker-compose build

docker-compose-run:
	docker-compose run --rm macro-analyzer python macro_analyzer.py --files economic1.csv economic2.csv --report average-gdp

docker-compose-sample:
	docker-compose --profile sample up

docker-clean:
	docker rmi macro-analyzer 2>/dev/null || true
	docker-compose down --rmi all 2>/dev/null || true
	docker system prune -f

# Development workflow
dev-setup: install
	@echo "Development environment setup complete!"

ci-test: test docker-build
	@echo "CI tests passed!"
