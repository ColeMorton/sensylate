# Python + YAML + Makefile Framework

## Project Structure

```
project_name/
├── configs/                    # Configuration files
│   ├── data_extraction.yaml   # Snake_case for scripts
│   ├── feature_engineering.yaml
│   ├── model_training.yaml
│   ├── report_generation.yaml
│   ├── shared/                 # Shared configurations
│   │   ├── paths.yaml         # Common file paths
│   │   ├── database.yaml      # DB connections
│   │   └── logging.yaml       # Logging setup
│   └── environments/          # Environment-specific
│       ├── dev.yaml
│       ├── staging.yaml
│       └── prod.yaml
├── scripts/                   # Main script modules
│   ├── __init__.py
│   ├── data_extraction.py     # Match config names
│   ├── feature_engineering.py
│   ├── model_training.py
│   ├── report_generation.py
│   └── utils/                 # Utility modules
│       ├── __init__.py
│       ├── config_loader.py   # Config handling
│       ├── file_utils.py      # File operations
│       ├── logging_setup.py   # Logging configuration
│       └── validators.py      # Data validation
├── data/                      # Data storage hierarchy
│   ├── raw/                   # Unprocessed source data
│   │   ├── YYYY-MM-DD/        # Date-based organization
│   │   └── backups/
│   ├── interim/               # Intermediate processing
│   │   ├── cleaned/
│   │   └── transformed/
│   ├── processed/             # Final processed data
│   │   ├── features/
│   │   └── models/
│   └── external/              # External reference data
├── outputs/                   # Generated outputs
│   ├── reports/               # Generated reports
│   │   ├── html/
│   │   ├── pdf/
│   │   └── markdown/
│   ├── visualizations/        # Charts and plots
│   │   ├── png/
│   │   └── svg/
│   ├── exports/               # Data exports
│   │   ├── csv/
│   │   ├── json/
│   │   └── parquet/
│   └── logs/                  # Execution logs
│       ├── YYYY-MM-DD/
│       └── errors/
├── tests/                     # Test files
│   ├── test_data_extraction.py
│   └── fixtures/
├── docs/                      # Documentation
│   ├── README.md
│   ├── config_guide.md
│   └── workflow_examples.md
├── Makefile                   # Workflow orchestration
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore
└── README.md

```

## Naming Conventions

### Files and Directories
- **snake_case** for all Python files and directories
- **kebab-case** for Make targets
- **UPPERCASE** for environment variables
- **PascalCase** for classes only

### Configuration Files
- Match script names: `data_extraction.py` → `data_extraction.yaml`
- Environment suffix: `config_dev.yaml`, `config_prod.yaml`
- Descriptive prefixes: `shared_paths.yaml`, `db_connections.yaml`

### Data Files
- Include timestamps: `data_2024-06-06.csv`
- Descriptive suffixes: `_raw.csv`, `_cleaned.csv`, `_final.parquet`
- Consistent formats: ISO dates (YYYY-MM-DD)

## Script Template with Best Practices

```python
#!/usr/bin/env python3
"""
Data extraction script with comprehensive configuration support.

Usage:
    python scripts/data_extraction.py --config configs/data_extraction.yaml
    python scripts/data_extraction.py --config configs/data_extraction.yaml --env prod
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

import yaml
from scripts.utils.config_loader import ConfigLoader
from scripts.utils.logging_setup import setup_logging


class DataExtractor:
    """Main data extraction class."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def extract_data(self) -> Path:
        """Extract data according to configuration."""
        # Implementation here
        output_path = Path(self.config['output']['file_path'])
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Data extracted to {output_path}")
        return output_path


def main(config: Dict[str, Any]) -> None:
    """Main execution function."""
    extractor = DataExtractor(config)
    output_file = extractor.extract_data()
    
    # Print output for Make dependency tracking
    print(f"OUTPUT_FILE={output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", 
        required=True,
        help="Path to YAML configuration file"
    )
    parser.add_argument(
        "--env",
        choices=['dev', 'staging', 'prod'],
        default='dev',
        help="Environment configuration"
    )
    parser.add_argument(
        "--output-file",
        help="Override output file path"
    )
    parser.add_argument(
        "--log-level",
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration with environment overlay
        config_loader = ConfigLoader()
        config = config_loader.load_with_environment(
            args.config, 
            args.env
        )
        
        # Setup logging
        setup_logging(
            level=args.log_level,
            log_file=config.get('logging', {}).get('file')
        )
        
        # Override with CLI arguments
        if args.output_file:
            config['output']['file_path'] = args.output_file
            
        main(config)
        
    except Exception as e:
        logging.error(f"Script failed: {e}")
        sys.exit(1)
```

## Configuration Structure

### Base Script Config (`configs/data_extraction.yaml`)
```yaml
# Data Extraction Configuration
metadata:
  name: "Data Extraction Pipeline"
  version: "1.0.0"
  description: "Extract raw data from multiple sources"

input:
  database:
    connection_string: "${DB_CONNECTION_STRING}"
    timeout: 30
  api:
    endpoint: "https://api.example.com/data"
    batch_size: 1000

output:
  file_path: "data/raw/extracted_data_{timestamp}.parquet"
  format: "parquet"
  compression: "snappy"

processing:
  validate_schema: true
  remove_duplicates: true
  max_retries: 3

logging:
  level: "INFO"
  file: "outputs/logs/data_extraction_{date}.log"
```

### Shared Configuration (`configs/shared/paths.yaml`)
```yaml
# Shared path configurations
base_paths:
  data_root: "data"
  output_root: "outputs"
  logs_root: "outputs/logs"

data_paths:
  raw: "${base_paths.data_root}/raw"
  interim: "${base_paths.data_root}/interim"
  processed: "${base_paths.data_root}/processed"
  external: "${base_paths.data_root}/external"

output_paths:
  reports: "${output_root}/reports"
  visualizations: "${output_root}/visualizations"
  exports: "${output_root}/exports"
```

## Makefile with Dependencies

```makefile
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
	@echo "  generate-report  - Generate final report"
	@echo "  full-pipeline    - Run complete pipeline"
	@echo "  clean           - Clean generated files"

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

.PHONY: generate-report
generate-report: $(OUTPUT_DIR)/reports/analysis_report_$(TIMESTAMP).html

$(OUTPUT_DIR)/reports/analysis_report_$(TIMESTAMP).html: $(DATA_DIR)/processed/features_$(TIMESTAMP).parquet
	$(PYTHON) scripts/report_generation.py \
		--config $(CONFIG_DIR)/report_generation.yaml \
		--input $< \
		--env $(ENV)

# Pipeline targets
.PHONY: full-pipeline
full-pipeline: extract-data process-data generate-report
	@echo "Pipeline completed successfully"

# Development shortcuts
.PHONY: dev-pipeline
dev-pipeline:
	$(MAKE) full-pipeline ENV=dev

.PHONY: prod-pipeline
prod-pipeline:
	$(MAKE) full-pipeline ENV=prod

# Utility targets
.PHONY: clean
clean:
	rm -rf $(DATA_DIR)/interim/*
	rm -rf $(OUTPUT_DIR)/logs/*
	rm -rf $(OUTPUT_DIR)/reports/*

.PHONY: clean-all
clean-all:
	rm -rf $(DATA_DIR)/raw/*
	rm -rf $(DATA_DIR)/interim/*
	rm -rf $(DATA_DIR)/processed/*
	rm -rf $(OUTPUT_DIR)/*

# Testing
.PHONY: test
test:
	$(PYTHON) -m pytest tests/ -v

# Environment setup
.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: install-dev
install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
```

## Best Practices

### Configuration Management
1. **Environment Separation**: Use environment-specific configs that overlay base configs
2. **Variable Substitution**: Support environment variables in YAML with `${VAR_NAME}`
3. **Validation**: Validate configs on load with schema validation
4. **Secrets**: Store sensitive data in environment variables, not configs

### Script Design
1. **Single Responsibility**: Each script should do one thing well
2. **Configurable I/O**: All input/output paths should be configurable
3. **Error Handling**: Comprehensive error handling with meaningful messages
4. **Logging**: Structured logging with different levels
5. **Idempotency**: Scripts should be safe to re-run

### File Organization
1. **Atomic Outputs**: Write to temporary files, then rename to final location
2. **Timestamps**: Include timestamps in output files for traceability
3. **Backup Strategy**: Keep backups of critical intermediate files
4. **Cleanup**: Provide cleanup targets in Makefile

### Workflow Management
1. **Dependencies**: Use Make dependencies to rebuild only what's needed
2. **Parallel Execution**: Use `make -j` for parallel execution where possible
3. **Error Propagation**: Ensure failures stop the pipeline
4. **Status Reporting**: Print clear success/failure messages

This framework provides a robust foundation for data processing pipelines while maintaining flexibility and following Python ecosystem conventions.