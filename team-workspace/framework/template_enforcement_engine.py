#!/usr/bin/env python3
"""
Template Enforcement Engine
Ensures consistent output formatting and metadata standards across all commands
"""

import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class TemplateStrictness(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    STRICT = "strict"

class ValidationSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationResult:
    """Result of template validation"""
    valid: bool
    severity: ValidationSeverity
    message: str
    rule_name: str
    location: Optional[str] = None
    suggestion: Optional[str] = None

@dataclass
class TemplateCompliance:
    """Template compliance assessment"""
    command: str
    overall_score: float
    compliance_percentage: float
    validation_results: List[ValidationResult]
    template_applied: bool
    fixes_applied: int
    timestamp: datetime

class TemplateEnforcementEngine:
    """Enforces consistent output formatting and metadata standards"""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.commands_path = Path(".claude/commands")
        self.templates_path = self.workspace_path / "framework" / "templates"
        self.templates_path.mkdir(parents=True, exist_ok=True)

        # Load template definitions
        self.template_definitions = self._load_template_definitions()

        # Initialize validation rules
        self.validation_rules = self._initialize_validation_rules()

        # Compliance tracking
        self.compliance_history = {}

    def enforce_template_compliance(self, command: str, content: str,
                                  output_type: str = "markdown") -> TemplateCompliance:
        """Enforce template compliance for command output"""

        print(f"🔍 Enforcing template compliance for {command} ({output_type})")

        # Load command's template enforcement configuration
        enforcement_config = self._load_enforcement_config(command)

        if not enforcement_config.get("enabled", False):
            return TemplateCompliance(
                command=command,
                overall_score=1.0,
                compliance_percentage=100.0,
                validation_results=[],
                template_applied=False,
                fixes_applied=0,
                timestamp=datetime.now()
            )

        # Validate against template rules
        validation_results = self._validate_content(command, content, output_type, enforcement_config)

        # Apply automatic fixes where possible
        fixed_content, fixes_applied = self._apply_automatic_fixes(content, validation_results, output_type)

        # Re-validate after fixes
        if fixes_applied > 0:
            validation_results = self._validate_content(command, fixed_content, output_type, enforcement_config)

        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(validation_results)

        compliance = TemplateCompliance(
            command=command,
            overall_score=compliance_score,
            compliance_percentage=compliance_score * 100,
            validation_results=validation_results,
            template_applied=True,
            fixes_applied=fixes_applied,
            timestamp=datetime.now()
        )

        # Record compliance history
        self._record_compliance(compliance)

        return compliance

    def generate_template_for_command(self, command: str, command_info: Dict[str, Any]) -> Dict[str, str]:
        """Generate templates for command based on its characteristics"""

        templates = {}
        output_types = command_info.get("template_requirements", {}).get("output_types", ["markdown"])

        for output_type in output_types:
            if output_type == "markdown":
                templates["markdown"] = self._generate_markdown_template(command, command_info)
            elif output_type == "json":
                templates["json"] = self._generate_json_template(command, command_info)
            elif output_type == "report":
                templates["report"] = self._generate_report_template(command, command_info)

        # Save templates
        self._save_command_templates(command, templates)

        return templates

    def _validate_content(self, command: str, content: str, output_type: str,
                         config: Dict[str, Any]) -> List[ValidationResult]:
        """Validate content against template rules"""

        results = []
        strictness = TemplateStrictness(config.get("strictness", "medium"))
        validation_rules = config.get("validation_rules", [])

        # Apply validation rules
        for rule in validation_rules:
            rule_type = rule["type"]

            if rule_type == "markdown_structure" and output_type == "markdown":
                results.extend(self._validate_markdown_structure(content, rule))
            elif rule_type == "json_schema" and output_type == "json":
                results.extend(self._validate_json_schema(content, rule))
            elif rule_type == "report_template" and output_type == "report":
                results.extend(self._validate_report_template(content, rule))
            elif rule_type == "metadata_headers":
                results.extend(self._validate_metadata_headers(content, rule))

        # Apply universal validation rules
        results.extend(self._validate_universal_standards(content, output_type, strictness))

        return results

    def _validate_markdown_structure(self, content: str, rule: Dict[str, Any]) -> List[ValidationResult]:
        """Validate markdown structure and formatting"""

        results = []

        # Check for required heading structure
        lines = content.split('\n')

        # Must start with H1
        if not lines or not lines[0].startswith('# '):
            results.append(ValidationResult(
                valid=False,
                severity=ValidationSeverity.ERROR,
                message="Markdown must start with H1 heading",
                rule_name="markdown_h1_required",
                suggestion="Add '# Title' as the first line"
            ))

        # Check heading hierarchy
        heading_levels = []
        for i, line in enumerate(lines):
            if line.startswith('#'):
                level = len(line.split()[0])
                heading_levels.append((level, i + 1))

        for i in range(1, len(heading_levels)):
            prev_level, prev_line = heading_levels[i-1]
            curr_level, curr_line = heading_levels[i]

            if curr_level > prev_level + 1:
                results.append(ValidationResult(
                    valid=False,
                    severity=ValidationSeverity.WARNING,
                    message=f"Heading level jump from H{prev_level} to H{curr_level}",
                    rule_name="heading_hierarchy",
                    location=f"line {curr_line}",
                    suggestion=f"Use H{prev_level + 1} instead of H{curr_level}"
                ))

        # Check for consistent formatting
        if '**' in content and '*' in content.replace('**', ''):
            results.append(ValidationResult(
                valid=False,
                severity=ValidationSeverity.INFO,
                message="Mixed bold formatting styles detected",
                rule_name="consistent_formatting",
                suggestion="Use consistent ** for bold formatting"
            ))

        return results

    def _validate_json_schema(self, content: str, rule: Dict[str, Any]) -> List[ValidationResult]:
        """Validate JSON content against schema"""

        results = []

        try:
            data = json.loads(content)

            # Basic JSON structure validation
            required_fields = ["timestamp", "command", "status"]
            for field in required_fields:
                if field not in data:
                    results.append(ValidationResult(
                        valid=False,
                        severity=ValidationSeverity.ERROR,
                        message=f"Required field '{field}' missing",
                        rule_name="json_required_fields",
                        suggestion=f"Add '{field}' field to JSON output"
                    ))

            # Validate timestamp format
            if "timestamp" in data:
                try:
                    datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
                except ValueError:
                    results.append(ValidationResult(
                        valid=False,
                        severity=ValidationSeverity.ERROR,
                        message="Invalid timestamp format",
                        rule_name="timestamp_format",
                        suggestion="Use ISO format: YYYY-MM-DDTHH:MM:SS"
                    ))

        except json.JSONDecodeError as e:
            results.append(ValidationResult(
                valid=False,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid JSON format: {str(e)}",
                rule_name="json_syntax",
                suggestion="Fix JSON syntax errors"
            ))

        return results

    def _validate_report_template(self, content: str, rule: Dict[str, Any]) -> List[ValidationResult]:
        """Validate report template structure"""

        results = []

        # Check for required report sections
        required_sections = [
            "Executive Summary",
            "Analysis",
            "Recommendations",
            "Conclusion"
        ]

        content_lower = content.lower()
        for section in required_sections:
            if section.lower() not in content_lower:
                results.append(ValidationResult(
                    valid=False,
                    severity=ValidationSeverity.WARNING,
                    message=f"Missing required section: {section}",
                    rule_name="report_sections",
                    suggestion=f"Add '{section}' section to report"
                ))

        return results

    def _validate_metadata_headers(self, content: str, rule: Dict[str, Any]) -> List[ValidationResult]:
        """Validate metadata headers"""

        results = []
        lines = content.split('\n')

        # Check for metadata at the beginning
        has_metadata = False
        if len(lines) > 3:
            first_lines = '\n'.join(lines[:5])
            if any(pattern in first_lines.lower() for pattern in ['created:', 'author:', 'date:', 'version:']):
                has_metadata = True

        if not has_metadata:
            results.append(ValidationResult(
                valid=False,
                severity=ValidationSeverity.WARNING,
                message="No metadata headers found",
                rule_name="metadata_headers",
                suggestion="Add metadata headers at the beginning (Created, Author, Date, etc.)"
            ))

        return results

    def _validate_universal_standards(self, content: str, output_type: str,
                                    strictness: TemplateStrictness) -> List[ValidationResult]:
        """Apply universal validation standards"""

        results = []

        # Check content length
        if len(content) < 50:
            results.append(ValidationResult(
                valid=False,
                severity=ValidationSeverity.WARNING,
                message="Content appears too short",
                rule_name="minimum_length",
                suggestion="Provide more detailed content"
            ))

        # Check for placeholder text
        placeholders = ["TODO", "FIXME", "TBD", "PLACEHOLDER", "[INSERT", "XXX"]
        for placeholder in placeholders:
            if placeholder in content.upper():
                results.append(ValidationResult(
                    valid=False,
                    severity=ValidationSeverity.ERROR,
                    message=f"Placeholder text found: {placeholder}",
                    rule_name="no_placeholders",
                    suggestion="Replace placeholder with actual content"
                ))

        # Check for consistent line endings
        if '\r\n' in content and '\n' in content.replace('\r\n', ''):
            results.append(ValidationResult(
                valid=False,
                severity=ValidationSeverity.INFO,
                message="Inconsistent line endings detected",
                rule_name="line_endings",
                suggestion="Use consistent line endings (preferably \\n)"
            ))

        return results

    def _apply_automatic_fixes(self, content: str, validation_results: List[ValidationResult],
                             output_type: str) -> tuple[str, int]:
        """Apply automatic fixes for validation issues"""

        fixed_content = content
        fixes_applied = 0

        for result in validation_results:
            if result.severity == ValidationSeverity.INFO:
                # Apply info-level fixes
                if result.rule_name == "line_endings":
                    fixed_content = fixed_content.replace('\r\n', '\n')
                    fixes_applied += 1
                elif result.rule_name == "consistent_formatting":
                    # Fix mixed bold formatting (simple case)
                    fixed_content = re.sub(r'\*([^*]+)\*(?!\*)', r'**\1**', fixed_content)
                    fixes_applied += 1

        # Add metadata headers if missing and output is markdown
        if output_type == "markdown":
            needs_metadata = any(r.rule_name == "metadata_headers" for r in validation_results)
            if needs_metadata and not fixed_content.startswith('---'):
                metadata = f"""---
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated: AI Command Framework
---

"""
                fixed_content = metadata + fixed_content
                fixes_applied += 1

        return fixed_content, fixes_applied

    def _calculate_compliance_score(self, validation_results: List[ValidationResult]) -> float:
        """Calculate overall compliance score"""

        if not validation_results:
            return 1.0

        total_score = 0
        max_score = 0

        for result in validation_results:
            max_score += 1

            if result.valid:
                total_score += 1
            else:
                # Partial credit based on severity
                if result.severity == ValidationSeverity.INFO:
                    total_score += 0.8
                elif result.severity == ValidationSeverity.WARNING:
                    total_score += 0.5
                # ERROR gets 0 points

        return total_score / max_score if max_score > 0 else 1.0

    def _generate_markdown_template(self, command: str, command_info: Dict[str, Any]) -> str:
        """Generate markdown template for command"""

        template = f"""---
Created: {{{{ timestamp }}}}
Command: {command}
Type: {command_info.get('command_type', 'utility')}
Complexity: {command_info.get('complexity', 'medium')}
---

# {command.replace('_', ' ').title()} Output

## Executive Summary

{{{{ executive_summary }}}}

## Analysis

{{{{ analysis_content }}}}

"""

        # Add command-specific sections
        if command_info.get('command_type') == 'analysis':
            template += """## Key Findings

{{ key_findings }}

## Confidence Assessment

{{ confidence_assessment }}

## Recommendations

{{ recommendations }}

"""
        elif command_info.get('command_type') == 'content':
            template += """## Content Overview

{{ content_overview }}

## Quality Metrics

{{ quality_metrics }}

## Optimization Suggestions

{{ optimization_suggestions }}

"""
        elif command_info.get('command_type') == 'trading':
            template += """## Trading Analysis

{{ trading_analysis }}

## Risk Assessment

{{ risk_assessment }}

## Action Items

{{ action_items }}

"""

        template += """## Technical Details

{{ technical_details }}

## Performance Metrics

- Execution Time: {{ execution_time }}
- Quality Score: {{ quality_score }}
- Confidence Level: {{ confidence_level }}

---
*Generated by AI Command Framework - Universal Evaluation System*
"""

        return template

    def _generate_json_template(self, command: str, command_info: Dict[str, Any]) -> str:
        """Generate JSON template for command"""

        template = {
            "timestamp": "{{ timestamp }}",
            "command": command,
            "type": command_info.get('command_type', 'utility'),
            "complexity": command_info.get('complexity', 'medium'),
            "status": "{{ status }}",
            "execution_time": "{{ execution_time }}",
            "results": {
                "summary": "{{ summary }}",
                "details": "{{ details }}"
            },
            "quality_metrics": {
                "score": "{{ quality_score }}",
                "confidence": "{{ confidence_level }}"
            },
            "metadata": {
                "generated_by": "AI Command Framework",
                "version": "1.0"
            }
        }

        return json.dumps(template, indent=2)

    def _generate_report_template(self, command: str, command_info: Dict[str, Any]) -> str:
        """Generate report template for command"""

        template = f"""# {command.replace('_', ' ').title()} Report

**Report Date:** {{{{ report_date }}}}
**Generated by:** AI Command Framework
**Command Type:** {command_info.get('command_type', 'utility')}

## Executive Summary

{{{{ executive_summary }}}}

## Analysis

{{{{ detailed_analysis }}}}

## Key Findings

{{{{ key_findings }}}}

## Recommendations

{{{{ recommendations }}}}

## Technical Details

{{{{ technical_details }}}}

## Appendix

{{{{ appendix_content }}}}

---
**Report Classification:** Internal Use
**Quality Assurance:** Universal Evaluation Framework
**Generated:** {{{{ timestamp }}}}
"""

        return template

    def _load_enforcement_config(self, command: str) -> Dict[str, Any]:
        """Load template enforcement configuration for command"""

        eval_file = self.commands_path / f"{command}.eval.yaml"

        if eval_file.exists():
            try:
                with open(eval_file, 'r') as f:
                    manifest = yaml.safe_load(f)
                return manifest.get("evaluation", {}).get("template_enforcement", {})
            except Exception:
                pass

        return {"enabled": False}

    def _save_command_templates(self, command: str, templates: Dict[str, str]):
        """Save templates for command"""

        command_templates_path = self.templates_path / command
        command_templates_path.mkdir(exist_ok=True)

        for output_type, template_content in templates.items():
            template_file = command_templates_path / f"{output_type}_template.{output_type}"

            with open(template_file, 'w') as f:
                f.write(template_content)

    def _record_compliance(self, compliance: TemplateCompliance):
        """Record compliance assessment for tracking"""

        if compliance.command not in self.compliance_history:
            self.compliance_history[compliance.command] = []

        self.compliance_history[compliance.command].append({
            "timestamp": compliance.timestamp.isoformat(),
            "score": compliance.overall_score,
            "percentage": compliance.compliance_percentage,
            "fixes_applied": compliance.fixes_applied,
            "validation_count": len(compliance.validation_results)
        })

        # Keep only last 10 assessments per command
        if len(self.compliance_history[compliance.command]) > 10:
            self.compliance_history[compliance.command] = self.compliance_history[compliance.command][-10:]

    def _load_template_definitions(self) -> Dict[str, Any]:
        """Load template definitions"""

        # Return default template definitions
        return {
            "markdown": {
                "required_sections": ["# Title", "## Summary"],
                "metadata_required": True,
                "max_heading_depth": 4
            },
            "json": {
                "required_fields": ["timestamp", "command", "status"],
                "schema_validation": True
            },
            "report": {
                "required_sections": ["Executive Summary", "Analysis", "Recommendations"],
                "formal_structure": True
            }
        }

    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize validation rules"""

        return {
            "universal": [
                {"type": "no_placeholders", "severity": "error"},
                {"type": "minimum_length", "severity": "warning"},
                {"type": "line_endings", "severity": "info"}
            ],
            "markdown": [
                {"type": "heading_structure", "severity": "warning"},
                {"type": "consistent_formatting", "severity": "info"}
            ],
            "json": [
                {"type": "syntax_validation", "severity": "error"},
                {"type": "schema_compliance", "severity": "error"}
            ]
        }

    def get_compliance_metrics(self) -> Dict[str, Any]:
        """Get overall template compliance metrics"""

        if not self.compliance_history:
            return {"status": "no_data", "commands_tracked": 0}

        total_assessments = sum(len(history) for history in self.compliance_history.values())

        # Calculate average compliance
        all_scores = []
        for command_history in self.compliance_history.values():
            all_scores.extend([entry["score"] for entry in command_history])

        avg_compliance = sum(all_scores) / len(all_scores) if all_scores else 0.0

        # Calculate improvement trends
        improving_commands = 0
        for command_history in self.compliance_history.values():
            if len(command_history) >= 2:
                recent_avg = sum(entry["score"] for entry in command_history[-3:]) / min(3, len(command_history))
                older_avg = sum(entry["score"] for entry in command_history[:-3]) / max(1, len(command_history) - 3)
                if recent_avg > older_avg:
                    improving_commands += 1

        return {
            "status": "active",
            "commands_tracked": len(self.compliance_history),
            "total_assessments": total_assessments,
            "average_compliance": avg_compliance,
            "improving_commands": improving_commands,
            "compliance_trend": "improving" if improving_commands > len(self.compliance_history) / 2 else "stable"
        }

def main():
    """Test template enforcement engine"""
    print("🎨 TEMPLATE ENFORCEMENT ENGINE")
    print("Testing template compliance validation")
    print("=" * 50)

    engine = TemplateEnforcementEngine()

    # Test with sample content
    test_content = """# Sample Analysis

This is a test analysis with some content.

## Results

The results are placeholder for now.

TODO: Add more detailed analysis here.
"""

    compliance = engine.enforce_template_compliance("test_command", test_content, "markdown")

    print(f"Compliance Score: {compliance.overall_score:.2f}")
    print(f"Compliance Percentage: {compliance.compliance_percentage:.1f}%")
    print(f"Fixes Applied: {compliance.fixes_applied}")

    for result in compliance.validation_results:
        severity_icon = "❌" if result.severity == ValidationSeverity.ERROR else "⚠️" if result.severity == ValidationSeverity.WARNING else "ℹ️"
        print(f"   {severity_icon} {result.message}")

if __name__ == "__main__":
    main()
