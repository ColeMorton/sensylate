"""
Validation Context Provider for Data Quality and Compliance

This provider handles all validation concerns including data quality assessment,
format validation, confidence scoring, and compliance checking. It abstracts
validation logic from commands, enabling consistent quality standards across
all command outputs.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum

from ..base_context import ValidationContext, QualityGate


logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Validation issue severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationResult:
    """Result of a validation check"""
    is_valid: bool
    confidence_score: float
    issues: List['ValidationIssue']
    metadata: Dict[str, Any]

    @property
    def has_errors(self) -> bool:
        """Check if result has error-level issues"""
        return any(issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]
                  for issue in self.issues)

    @property
    def has_warnings(self) -> bool:
        """Check if result has warning-level issues"""
        return any(issue.severity == ValidationSeverity.WARNING for issue in self.issues)


@dataclass
class ValidationIssue:
    """Individual validation issue"""
    field: str
    message: str
    severity: ValidationSeverity
    value: Any = None
    expected: Any = None
    code: str = None


class ValidationError(Exception):
    """Raised when validation fails critically"""
    pass


class ValidationContextProvider:
    """
    Validation provider for Sensylate commands.

    This provider centralizes all validation logic, providing consistent
    data quality assessment across commands. It handles:

    - Data format validation
    - Confidence scoring
    - Quality gate enforcement
    - Financial data specific validation
    - Institutional compliance checking

    Usage:
        provider = ValidationContextProvider(validation_context)
        result = provider.validate_fundamental_data(data)
        if not result.is_valid:
            raise ValidationError("Data validation failed")
    """

    def __init__(self, validation_context: ValidationContext):
        self.context = validation_context
        self.validation_rules = self._load_validation_rules()

    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules based on quality gate"""
        return {
            "fundamental_analysis": {
                "required_fields": [
                    "market_data", "financial_metrics", "company_intelligence"
                ],
                "market_data_fields": [
                    "current_price", "market_cap", "enterprise_value", "volume"
                ],
                "financial_fields": [
                    "revenue_ttm", "net_income", "earnings_per_share", "pe_ratio"
                ],
                "format_rules": {
                    "market_cap": {"type": "int", "min": 0},
                    "pe_ratio": {"type": "float", "min": 0, "precision": 2},
                    "profit_margin": {"type": "float", "min": 0, "max": 1}
                }
            },
            "trading_analysis": {
                "required_fields": [
                    "signals", "portfolio_metrics", "performance_data"
                ],
                "signal_fields": [
                    "action", "confidence", "price_target", "stop_loss"
                ]
            }
        }

    def validate_fundamental_data(self, data: Dict[str, Any], ticker: str = None) -> ValidationResult:
        """
        Validate fundamental analysis data structure and content.

        Args:
            data: Fundamental analysis data to validate
            ticker: Optional ticker symbol for context

        Returns:
            ValidationResult with validation outcome
        """
        issues = []
        confidence_scores = []

        # Validate required structure
        structure_issues = self._validate_structure(
            data,
            self.validation_rules["fundamental_analysis"]["required_fields"]
        )
        issues.extend(structure_issues)

        # Validate market data
        if "market_data" in data:
            market_issues, market_confidence = self._validate_market_data(data["market_data"])
            issues.extend(market_issues)
            confidence_scores.append(market_confidence)

        # Validate financial metrics
        if "financial_metrics" in data:
            financial_issues, financial_confidence = self._validate_financial_metrics(data["financial_metrics"])
            issues.extend(financial_issues)
            confidence_scores.append(financial_confidence)

        # Validate company intelligence
        if "company_intelligence" in data:
            intel_issues, intel_confidence = self._validate_company_intelligence(data["company_intelligence"])
            issues.extend(intel_issues)
            confidence_scores.append(intel_confidence)

        # Calculate overall confidence
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0

        # Apply quality gate requirements
        is_valid = self._check_quality_gate(issues, overall_confidence)

        return ValidationResult(
            is_valid=is_valid,
            confidence_score=overall_confidence,
            issues=issues,
            metadata={
                "ticker": ticker,
                "validation_timestamp": datetime.now().isoformat(),
                "quality_gate": self.context.quality_gates.value,
                "institutional_target": self.context.institutional_target
            }
        )

    def _validate_structure(self, data: Dict[str, Any], required_fields: List[str]) -> List[ValidationIssue]:
        """Validate data structure has required fields"""
        issues = []

        for field in required_fields:
            if field not in data:
                issues.append(ValidationIssue(
                    field=field,
                    message=f"Required field '{field}' is missing",
                    severity=ValidationSeverity.ERROR,
                    code="MISSING_REQUIRED_FIELD"
                ))
            elif data[field] is None:
                issues.append(ValidationIssue(
                    field=field,
                    message=f"Required field '{field}' is null",
                    severity=ValidationSeverity.ERROR,
                    code="NULL_REQUIRED_FIELD"
                ))

        return issues

    def _validate_market_data(self, market_data: Dict[str, Any]) -> tuple[List[ValidationIssue], float]:
        """Validate market data section"""
        issues = []
        confidence_factors = []

        required_fields = self.validation_rules["fundamental_analysis"]["market_data_fields"]

        # Check required fields
        for field in required_fields:
            if field not in market_data:
                issues.append(ValidationIssue(
                    field=f"market_data.{field}",
                    message=f"Missing market data field: {field}",
                    severity=ValidationSeverity.ERROR
                ))
                continue

            value = market_data[field]

            # Validate specific formats
            if field == "market_cap":
                if not isinstance(value, (int, float)) or value <= 0:
                    issues.append(ValidationIssue(
                        field=f"market_data.{field}",
                        message="Market cap must be positive number",
                        severity=ValidationSeverity.ERROR,
                        value=value
                    ))
                else:
                    # High confidence for proper integer format
                    confidence_factors.append(0.95 if isinstance(value, int) else 0.8)

            elif field == "current_price":
                if not isinstance(value, (int, float)) or value <= 0:
                    issues.append(ValidationIssue(
                        field=f"market_data.{field}",
                        message="Current price must be positive number",
                        severity=ValidationSeverity.ERROR,
                        value=value
                    ))
                else:
                    confidence_factors.append(0.9)

        # Check confidence field if present
        if "confidence" in market_data:
            confidence = market_data["confidence"]
            if isinstance(confidence, (int, float)) and 0 <= confidence <= 1:
                confidence_factors.append(confidence)
            else:
                issues.append(ValidationIssue(
                    field="market_data.confidence",
                    message="Confidence must be between 0 and 1",
                    severity=ValidationSeverity.WARNING,
                    value=confidence
                ))

        overall_confidence = sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5
        return issues, overall_confidence

    def _validate_financial_metrics(self, financial_data: Dict[str, Any]) -> tuple[List[ValidationIssue], float]:
        """Validate financial metrics section"""
        issues = []
        confidence_factors = []

        format_rules = self.validation_rules["fundamental_analysis"]["format_rules"]

        for field, rules in format_rules.items():
            if field not in financial_data:
                continue

            value = financial_data[field]

            # Type validation
            expected_type = rules.get("type")
            if expected_type == "int" and not isinstance(value, int):
                issues.append(ValidationIssue(
                    field=f"financial_metrics.{field}",
                    message=f"Field {field} must be integer",
                    severity=ValidationSeverity.ERROR,
                    value=value,
                    expected="integer"
                ))
                continue
            elif expected_type == "float" and not isinstance(value, (int, float)):
                issues.append(ValidationIssue(
                    field=f"financial_metrics.{field}",
                    message=f"Field {field} must be numeric",
                    severity=ValidationSeverity.ERROR,
                    value=value,
                    expected="float"
                ))
                continue

            # Range validation
            min_val = rules.get("min")
            max_val = rules.get("max")

            if min_val is not None and value < min_val:
                issues.append(ValidationIssue(
                    field=f"financial_metrics.{field}",
                    message=f"Field {field} below minimum: {min_val}",
                    severity=ValidationSeverity.WARNING,
                    value=value,
                    expected=f">= {min_val}"
                ))

            if max_val is not None and value > max_val:
                issues.append(ValidationIssue(
                    field=f"financial_metrics.{field}",
                    message=f"Field {field} above maximum: {max_val}",
                    severity=ValidationSeverity.WARNING,
                    value=value,
                    expected=f"<= {max_val}"
                ))

            # Precision validation for institutional compliance
            if expected_type == "float" and rules.get("precision"):
                precision = rules["precision"]
                decimal_places = len(str(value).split(".")[-1]) if "." in str(value) else 0
                if decimal_places != precision:
                    severity = ValidationSeverity.ERROR if self.context.quality_gates == QualityGate.INSTITUTIONAL else ValidationSeverity.WARNING
                    issues.append(ValidationIssue(
                        field=f"financial_metrics.{field}",
                        message=f"Field {field} requires {precision} decimal places",
                        severity=severity,
                        value=value,
                        expected=f"{precision} decimal places"
                    ))

            # High confidence for properly formatted values
            confidence_factors.append(0.9)

        # Check confidence field
        if "confidence" in financial_data:
            confidence = financial_data["confidence"]
            if isinstance(confidence, (int, float)) and 0 <= confidence <= 1:
                confidence_factors.append(confidence)

        overall_confidence = sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5
        return issues, overall_confidence

    def _validate_company_intelligence(self, intel_data: Dict[str, Any]) -> tuple[List[ValidationIssue], float]:
        """Validate company intelligence section"""
        issues = []
        confidence_factors = []

        # Validate business model
        if "business_model" in intel_data:
            bm = intel_data["business_model"]
            if not isinstance(bm, dict):
                issues.append(ValidationIssue(
                    field="company_intelligence.business_model",
                    message="Business model must be object",
                    severity=ValidationSeverity.ERROR,
                    value=type(bm).__name__
                ))
            else:
                # Check for key business model fields
                required_bm_fields = ["revenue_streams", "operational_model"]
                for field in required_bm_fields:
                    if field not in bm:
                        issues.append(ValidationIssue(
                            field=f"company_intelligence.business_model.{field}",
                            message=f"Missing business model field: {field}",
                            severity=ValidationSeverity.WARNING
                        ))

                if "confidence" in bm and isinstance(bm["confidence"], (int, float)):
                    confidence_factors.append(bm["confidence"])

        # Validate financial statements
        if "financial_statements" in intel_data:
            fs = intel_data["financial_statements"]
            if isinstance(fs, dict):
                required_statements = ["income_statement", "balance_sheet", "cash_flow"]
                for statement in required_statements:
                    if statement not in fs:
                        issues.append(ValidationIssue(
                            field=f"company_intelligence.financial_statements.{statement}",
                            message=f"Missing financial statement: {statement}",
                            severity=ValidationSeverity.WARNING
                        ))

                if "confidence" in fs and isinstance(fs["confidence"], (int, float)):
                    confidence_factors.append(fs["confidence"])

        overall_confidence = sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.7
        return issues, overall_confidence

    def _check_quality_gate(self, issues: List[ValidationIssue], confidence: float) -> bool:
        """Check if validation meets quality gate requirements"""
        # Check confidence threshold
        if not self.context.meets_confidence_threshold(confidence):
            return False

        # Check for critical errors
        has_critical = any(issue.severity == ValidationSeverity.CRITICAL for issue in issues)
        if has_critical:
            return False

        # Quality gate specific rules
        if self.context.quality_gates == QualityGate.INSTITUTIONAL:
            # Institutional requires very high standards
            has_errors = any(issue.severity == ValidationSeverity.ERROR for issue in issues)
            return not has_errors and confidence >= self.context.institutional_target / 10.0

        elif self.context.quality_gates == QualityGate.STRICT:
            # Strict allows minimal errors
            error_count = sum(1 for issue in issues if issue.severity == ValidationSeverity.ERROR)
            return error_count <= 1

        elif self.context.quality_gates == QualityGate.STANDARD:
            # Standard allows some errors
            error_count = sum(1 for issue in issues if issue.severity == ValidationSeverity.ERROR)
            return error_count <= 3

        else:  # MINIMAL
            # Minimal only blocks critical errors
            return not has_critical

    def validate_ticker_symbol(self, ticker: str) -> ValidationResult:
        """Validate ticker symbol format"""
        issues = []

        if not ticker:
            issues.append(ValidationIssue(
                field="ticker",
                message="Ticker symbol is required",
                severity=ValidationSeverity.ERROR,
                code="MISSING_TICKER"
            ))
        elif not isinstance(ticker, str):
            issues.append(ValidationIssue(
                field="ticker",
                message="Ticker must be string",
                severity=ValidationSeverity.ERROR,
                value=type(ticker).__name__
            ))
        else:
            # Format validation
            ticker = ticker.strip().upper()
            if not ticker.isalnum():
                issues.append(ValidationIssue(
                    field="ticker",
                    message="Ticker must be alphanumeric",
                    severity=ValidationSeverity.ERROR,
                    value=ticker
                ))
            elif len(ticker) < 1 or len(ticker) > 5:
                issues.append(ValidationIssue(
                    field="ticker",
                    message="Ticker must be 1-5 characters",
                    severity=ValidationSeverity.WARNING,
                    value=ticker
                ))

        confidence = 1.0 if not issues else 0.5
        is_valid = len([i for i in issues if i.severity == ValidationSeverity.ERROR]) == 0

        return ValidationResult(
            is_valid=is_valid,
            confidence_score=confidence,
            issues=issues,
            metadata={"validated_ticker": ticker if isinstance(ticker, str) else None}
        )

    def validate_json_format(self, data: Any, schema: Dict[str, Any] = None) -> ValidationResult:
        """Validate JSON format and structure"""
        issues = []

        # Basic JSON validation
        try:
            json_str = json.dumps(data, default=str)
            json.loads(json_str)  # Validate round-trip
        except (TypeError, ValueError) as e:
            issues.append(ValidationIssue(
                field="json_format",
                message=f"Invalid JSON structure: {e}",
                severity=ValidationSeverity.CRITICAL,
                code="INVALID_JSON"
            ))

        # Schema validation if provided
        if schema and not issues:
            schema_issues = self._validate_json_schema(data, schema)
            issues.extend(schema_issues)

        confidence = 1.0 if not issues else 0.0
        is_valid = not any(i.severity == ValidationSeverity.CRITICAL for i in issues)

        return ValidationResult(
            is_valid=is_valid,
            confidence_score=confidence,
            issues=issues,
            metadata={"format_validation": True}
        )

    def _validate_json_schema(self, data: Any, schema: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate data against JSON schema (simplified)"""
        issues = []

        # This is a simplified schema validator
        # In production, consider using jsonschema library

        if "required" in schema:
            for required_field in schema["required"]:
                if not isinstance(data, dict) or required_field not in data:
                    issues.append(ValidationIssue(
                        field=required_field,
                        message=f"Required field missing: {required_field}",
                        severity=ValidationSeverity.ERROR,
                        code="SCHEMA_REQUIRED_FIELD"
                    ))

        return issues

    def get_validation_summary(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Get summary of multiple validation results"""
        total_validations = len(results)
        valid_count = sum(1 for r in results if r.is_valid)

        all_issues = []
        all_confidences = []

        for result in results:
            all_issues.extend(result.issues)
            all_confidences.append(result.confidence_score)

        severity_counts = {
            "critical": sum(1 for i in all_issues if i.severity == ValidationSeverity.CRITICAL),
            "error": sum(1 for i in all_issues if i.severity == ValidationSeverity.ERROR),
            "warning": sum(1 for i in all_issues if i.severity == ValidationSeverity.WARNING),
            "info": sum(1 for i in all_issues if i.severity == ValidationSeverity.INFO)
        }

        return {
            "total_validations": total_validations,
            "valid_count": valid_count,
            "success_rate": valid_count / total_validations if total_validations > 0 else 0,
            "average_confidence": sum(all_confidences) / len(all_confidences) if all_confidences else 0,
            "issue_counts": severity_counts,
            "quality_gate": self.context.quality_gates.value,
            "institutional_compliance": valid_count == total_validations and severity_counts["error"] == 0,
            "summary_timestamp": datetime.now().isoformat()
        }
