# Variables
PYTHON := python3
CONFIG_DIR := configs
DATA_DIR := data
OUTPUT_DIR := outputs
TIMESTAMP := $(shell date +%Y-%m-%d_%H-%M-%S)

# Default environment
ENV ?= dev

# Help target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  extract-data     - Extract raw data"
	@echo "  process-data     - Process extracted data"
	@echo "  train-model      - Train machine learning model"
	@echo "  generate-report  - Generate final report"
	@echo "  generate-dashboard - Generate performance dashboard"
	@echo "  full-pipeline    - Run complete pipeline"
	@echo "  clean           - Clean generated files"
	@echo "  test            - Run all tests"
	@echo "  test-collaboration - Run collaboration framework tests"
	@echo "  test-e2e        - Run end-to-end collaboration tests"
	@echo "  install         - Install dependencies"

# Individual script targets
.PHONY: extract-data
extract-data: $(DATA_DIR)/raw/extracted_data_$(TIMESTAMP).parquet

$(DATA_DIR)/raw/extracted_data_$(TIMESTAMP).parquet: $(CONFIG_DIR)/data_extraction.yaml
	$(PYTHON) scripts/data_extraction.py --config $< --env $(ENV)

.PHONY: process-data
process-data: $(DATA_DIR)/processed/features_$(TIMESTAMP).parquet

$(DATA_DIR)/processed/features_$(TIMESTAMP).parquet: $(DATA_DIR)/raw/extracted_data_$(TIMESTAMP).parquet
	$(PYTHON) scripts/feature_engineering.py \
		--config $(CONFIG_DIR)/feature_engineering.yaml \
		--input $< \
		--env $(ENV)

.PHONY: train-model
train-model: $(DATA_DIR)/processed/models/trained_model_$(TIMESTAMP).pkl

$(DATA_DIR)/processed/models/trained_model_$(TIMESTAMP).pkl: $(DATA_DIR)/processed/features_$(TIMESTAMP).parquet
	$(PYTHON) scripts/model_training.py \
		--config $(CONFIG_DIR)/model_training.yaml \
		--input $< \
		--env $(ENV)

.PHONY: generate-report
generate-report: $(OUTPUT_DIR)/reports/analysis_report_$(TIMESTAMP).html

$(OUTPUT_DIR)/reports/analysis_report_$(TIMESTAMP).html: $(DATA_DIR)/processed/features_$(TIMESTAMP).parquet
	$(PYTHON) scripts/report_generation.py \
		--config $(CONFIG_DIR)/report_generation.yaml \
		--input $< \
		--env $(ENV)

# Dashboard generation targets
# Integrated report generation (report + dashboard)
.PHONY: generate-report-with-dashboard
generate-report-with-dashboard: $(OUTPUT_DIR)/reports/analysis_report_$(TIMESTAMP).html $(OUTPUT_DIR)/dashboards/historical-performance-dashboard-light-$(TIMESTAMP).png

.PHONY: generate-report-integrated
generate-report-integrated:
	$(PYTHON) scripts/generate_report_with_dashboard.py \
		--report-config $(CONFIG_DIR)/report_generation.yaml \
		--dashboard-config $(CONFIG_DIR)/dashboard_generation.yaml \
		--input $(shell ls -t $(DATA_DIR)/processed/features*.parquet | head -1) \
		--env $(ENV) \
		--quiet

.PHONY: generate-dashboard
generate-dashboard: $(OUTPUT_DIR)/dashboards/historical-performance-dashboard-light-$(TIMESTAMP).png

$(OUTPUT_DIR)/dashboards/historical-performance-dashboard-light-$(TIMESTAMP).png: data/outputs/analysis_trade_history/HISTORICAL_PERFORMANCE_REPORT_$(TIMESTAMP).md
	$(PYTHON) scripts/dashboard_generator.py \
		--config $(CONFIG_DIR)/dashboard_generation.yaml \
		--input $< \
		--mode both \
		--env $(ENV) \
		--quiet

.PHONY: generate-dashboard-light
generate-dashboard-light: $(OUTPUT_DIR)/dashboards/historical-performance-dashboard-light-$(TIMESTAMP).png

.PHONY: generate-dashboard-dark
generate-dashboard-dark: $(OUTPUT_DIR)/dashboards/historical-performance-dashboard-dark-$(TIMESTAMP).png

$(OUTPUT_DIR)/dashboards/historical-performance-dashboard-dark-$(TIMESTAMP).png: data/outputs/analysis_trade_history/HISTORICAL_PERFORMANCE_REPORT_$(TIMESTAMP).md
	$(PYTHON) scripts/dashboard_generator.py \
		--config $(CONFIG_DIR)/dashboard_generation.yaml \
		--input $< \
		--mode dark \
		--env $(ENV) \
		--quiet

# Pipeline targets
.PHONY: full-pipeline
full-pipeline: extract-data process-data train-model generate-report
	@echo "Pipeline completed successfully"

.PHONY: full-pipeline-with-dashboard
full-pipeline-with-dashboard: extract-data process-data train-model generate-report generate-dashboard
	@echo "Pipeline with dashboard completed successfully"

# Development shortcuts
.PHONY: dev-pipeline
dev-pipeline:
	$(MAKE) full-pipeline ENV=dev

.PHONY: dev-pipeline-dashboard
dev-pipeline-dashboard:
	$(MAKE) full-pipeline-with-dashboard ENV=dev

.PHONY: staging-pipeline
staging-pipeline:
	$(MAKE) full-pipeline ENV=staging

.PHONY: staging-pipeline-dashboard
staging-pipeline-dashboard:
	$(MAKE) full-pipeline-with-dashboard ENV=staging

.PHONY: prod-pipeline
prod-pipeline:
	$(MAKE) full-pipeline ENV=prod

.PHONY: prod-pipeline-dashboard
prod-pipeline-dashboard:
	$(MAKE) full-pipeline-with-dashboard ENV=prod

# Quick dashboard generation (development)
.PHONY: quick-dashboard
quick-dashboard:
	$(PYTHON) scripts/dashboard_generator.py \
		--config $(CONFIG_DIR)/dashboard_generation.yaml \
		--input $(shell ls -t data/outputs/analysis_trade_history/*.md | head -1) \
		--mode both \
		--env dev \
		--log-level DEBUG

.PHONY: quick-dashboard-validate
quick-dashboard-validate:
	$(PYTHON) scripts/dashboard_generator.py \
		--config $(CONFIG_DIR)/dashboard_generation.yaml \
		--input $(shell ls -t data/outputs/analysis_trade_history/*.md | head -1) \
		--validate-only \
		--env dev

# Utility targets
.PHONY: clean
clean:
	rm -rf $(DATA_DIR)/interim/*
	rm -rf $(OUTPUT_DIR)/logs/*
	rm -rf $(OUTPUT_DIR)/reports/*
	rm -rf $(OUTPUT_DIR)/dashboards/*

.PHONY: clean-all
clean-all:
	rm -rf $(DATA_DIR)/raw/*
	rm -rf $(DATA_DIR)/interim/*
	rm -rf $(DATA_DIR)/processed/*
	rm -rf $(OUTPUT_DIR)/*

.PHONY: clean-dashboards
clean-dashboards:
	rm -rf data/outputs/dashboards/*
	@echo "Dashboard files cleaned"

# Testing
.PHONY: test
test:
	$(PYTHON) -m pytest tests/ -v

.PHONY: test-collaboration
test-collaboration:
	@echo "Running Command Collaboration Framework tests..."
	$(PYTHON) -m pytest tests/collaboration/ -v --tb=short

.PHONY: test-collaboration-verbose
test-collaboration-verbose:
	@echo "Running Command Collaboration Framework tests (verbose)..."
	$(PYTHON) -m pytest tests/collaboration/ -v -s --tb=long

.PHONY: test-collaboration-coverage
test-collaboration-coverage:
	@echo "Running Command Collaboration Framework tests with coverage..."
	$(PYTHON) -m pytest tests/collaboration/ --cov=team_workspace --cov-report=html --cov-report=term

.PHONY: test-e2e
test-e2e:
	@echo "Running end-to-end collaboration workflow tests..."
	$(PYTHON) -m pytest tests/collaboration/test_e2e_collaboration.py -v -s

.PHONY: test-coverage
test-coverage:
	$(PYTHON) -m pytest tests/ --cov=scripts --cov=team_workspace --cov-report=html

.PHONY: test-all
test-all: test test-collaboration
	@echo "All tests completed successfully"

# Environment setup
.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: install-dev
install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Validation targets
.PHONY: validate-configs
validate-configs:
	@echo "Validating configuration files..."
	@for config in $(CONFIG_DIR)/*.yaml; do \
		echo "Checking $$config"; \
		$(PYTHON) -c "import yaml; yaml.safe_load(open('$$config'))" || exit 1; \
	done
	@echo "All configs valid"

.PHONY: check-env-vars
check-env-vars:
	@echo "Checking required environment variables..."
	@$(PYTHON) -c "import os; \
		required = ['DB_CONNECTION_STRING', 'API_BASE_URL']; \
		missing = [v for v in required if not os.getenv(v)]; \
		print('Missing env vars:', missing) if missing else print('All env vars present'); \
		exit(1) if missing else exit(0)"

# Directory structure setup
.PHONY: setup-dirs
setup-dirs:
	mkdir -p $(DATA_DIR)/raw
	mkdir -p $(DATA_DIR)/interim/cleaned
	mkdir -p $(DATA_DIR)/interim/transformed
	mkdir -p $(DATA_DIR)/processed/features
	mkdir -p $(DATA_DIR)/processed/models
	mkdir -p $(DATA_DIR)/external
	mkdir -p $(OUTPUT_DIR)/reports/html
	mkdir -p $(OUTPUT_DIR)/reports/pdf
	mkdir -p $(OUTPUT_DIR)/reports/markdown
	mkdir -p $(OUTPUT_DIR)/visualizations/png
	mkdir -p $(OUTPUT_DIR)/visualizations/svg
	mkdir -p $(OUTPUT_DIR)/dashboards
	mkdir -p $(OUTPUT_DIR)/exports/csv
	mkdir -p $(OUTPUT_DIR)/exports/json
	mkdir -p $(OUTPUT_DIR)/exports/parquet
	mkdir -p $(OUTPUT_DIR)/logs
	mkdir -p tests/fixtures

# Linting and formatting
.PHONY: lint
lint:
	$(PYTHON) -m flake8 scripts/
	$(PYTHON) -m black --check scripts/

.PHONY: format
format:
	$(PYTHON) -m black scripts/
	$(PYTHON) -m isort scripts/

# Quick development targets
.PHONY: quick-extract
quick-extract:
	$(PYTHON) scripts/data_extraction.py \
		--config $(CONFIG_DIR)/data_extraction.yaml \
		--env dev \
		--log-level DEBUG

.PHONY: quick-process
quick-process: quick-extract
	$(PYTHON) scripts/feature_engineering.py \
		--config $(CONFIG_DIR)/feature_engineering.yaml \
		--input $(shell ls -t $(DATA_DIR)/raw/*.parquet | head -1) \
		--env dev \
		--log-level DEBUG
