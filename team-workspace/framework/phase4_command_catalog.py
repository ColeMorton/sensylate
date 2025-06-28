#!/usr/bin/env python3
"""
Phase 4 Command Catalog
Identifies and catalogs all commands for Universal Evaluation deployment
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class Phase4CommandCatalog:
    """Catalogs all commands for Phase 4 Universal Evaluation deployment"""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.commands_path = Path(".claude/commands")

    def catalog_all_commands(self) -> Dict[str, Any]:
        """Catalog all commands and their deployment status"""

        # Get all command files
        command_files = list(self.commands_path.glob("*.md"))

        # Commands already integrated in previous phases
        integrated_commands = {
            "fundamental_analysis": {
                "phase": "Phase 2",
                "status": "fully_integrated",
                "has_eval_manifest": True,
                "has_deps_manifest": True,
                "integration_quality": "comprehensive"
            },
            "social_media_content": {
                "phase": "Phase 2",
                "status": "fully_integrated",
                "has_eval_manifest": True,
                "has_deps_manifest": True,
                "integration_quality": "comprehensive"
            }
        }

        # Legacy Twitter commands (consolidated in Phase 2)
        legacy_commands = {
            "twitter_post": "consolidated_into_social_media_content",
            "twitter_post_strategy": "consolidated_into_social_media_content",
            "twitter_fundamental_analysis": "consolidated_into_social_media_content"
        }

        # Identify remaining commands for Phase 4
        remaining_commands = {}

        for cmd_file in command_files:
            command_name = cmd_file.stem

            # Skip already integrated and legacy commands
            if command_name in integrated_commands or command_name in legacy_commands:
                continue

            # Analyze command for deployment requirements
            command_info = self._analyze_command(cmd_file)
            remaining_commands[command_name] = command_info

        # Categorize by complexity and priority
        categorized_commands = self._categorize_commands(remaining_commands)

        catalog = {
            "timestamp": datetime.now().isoformat(),
            "total_commands": len(command_files),
            "integrated_commands": integrated_commands,
            "legacy_commands": legacy_commands,
            "remaining_commands": remaining_commands,
            "categorized_deployment": categorized_commands,
            "phase4_scope": {
                "target_commands": len(remaining_commands),
                "deployment_priority": self._calculate_deployment_priority(remaining_commands)
            }
        }

        return catalog

    def _analyze_command(self, cmd_file: Path) -> Dict[str, Any]:
        """Analyze command file for deployment requirements"""

        try:
            with open(cmd_file, 'r') as f:
                content = f.read()
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "complexity": "unknown"
            }

        analysis = {
            "file_path": str(cmd_file),
            "content_length": len(content),
            "complexity": self._assess_complexity(content),
            "command_type": self._determine_command_type(content),
            "dependencies": self._extract_dependencies(content),
            "evaluation_requirements": self._assess_evaluation_needs(content),
            "template_requirements": self._assess_template_needs(content),
            "deployment_priority": "medium"
        }

        # Set deployment priority based on analysis
        analysis["deployment_priority"] = self._calculate_command_priority(analysis)

        return analysis

    def _assess_complexity(self, content: str) -> str:
        """Assess command complexity level"""

        complexity_indicators = {
            "high": [
                "fundamental analysis", "technical analysis", "market data",
                "trading strategy", "financial modeling", "risk assessment",
                "portfolio", "backtesting", "optimization"
            ],
            "medium": [
                "content creation", "social media", "publishing", "formatting",
                "data processing", "report generation", "analysis"
            ],
            "low": [
                "simple", "basic", "utility", "helper", "format", "convert"
            ]
        }

        content_lower = content.lower()

        high_count = sum(1 for indicator in complexity_indicators["high"] if indicator in content_lower)
        medium_count = sum(1 for indicator in complexity_indicators["medium"] if indicator in content_lower)
        low_count = sum(1 for indicator in complexity_indicators["low"] if indicator in content_lower)

        if high_count >= 2:
            return "high"
        elif medium_count >= 2 or high_count >= 1:
            return "medium"
        else:
            return "low"

    def _determine_command_type(self, content: str) -> str:
        """Determine command type category"""

        content_lower = content.lower()

        if any(term in content_lower for term in ["architect", "planning", "implementation"]):
            return "development"
        elif any(term in content_lower for term in ["analysis", "fundamental", "technical", "data"]):
            return "analysis"
        elif any(term in content_lower for term in ["content", "social", "publish", "post"]):
            return "content"
        elif any(term in content_lower for term in ["trade", "trading", "history", "portfolio"]):
            return "trading"
        elif any(term in content_lower for term in ["business", "product", "owner", "management"]):
            return "management"
        else:
            return "utility"

    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract potential dependencies from command content"""

        dependencies = []
        content_lower = content.lower()

        # Common dependency patterns
        dependency_patterns = {
            "data_sources": ["yahoo finance", "market data", "financial data", "api"],
            "file_systems": ["file", "directory", "path", "output", "save"],
            "services": ["service", "external", "integration", "webhook"],
            "other_commands": ["command", "workflow", "pipeline", "process"]
        }

        for dep_type, patterns in dependency_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                dependencies.append(dep_type)

        return dependencies

    def _assess_evaluation_needs(self, content: str) -> Dict[str, Any]:
        """Assess evaluation requirements for command"""

        content_lower = content.lower()

        # Determine quality gates needed
        quality_gates = []

        if any(term in content_lower for term in ["data", "api", "external"]):
            quality_gates.append("dependency_validation")

        if any(term in content_lower for term in ["analysis", "recommendation", "decision"]):
            quality_gates.append("confidence_scoring")

        if any(term in content_lower for term in ["output", "file", "content", "result"]):
            quality_gates.append("output_validation")

        if any(term in content_lower for term in ["performance", "speed", "efficiency"]):
            quality_gates.append("performance_monitoring")

        # Determine evaluation complexity
        if len(quality_gates) >= 3:
            complexity = "comprehensive"
        elif len(quality_gates) >= 2:
            complexity = "standard"
        else:
            complexity = "basic"

        return {
            "complexity": complexity,
            "quality_gates": quality_gates,
            "confidence_scoring": "confidence" in content_lower or "score" in content_lower,
            "phase_0a_compatible": "evaluation" in content_lower or "enhance" in content_lower
        }

    def _assess_template_needs(self, content: str) -> Dict[str, Any]:
        """Assess template enforcement requirements"""

        content_lower = content.lower()

        output_types = []
        if any(term in content_lower for term in ["markdown", "md", "document"]):
            output_types.append("markdown")
        if any(term in content_lower for term in ["json", "data", "structured"]):
            output_types.append("json")
        if any(term in content_lower for term in ["report", "analysis", "summary"]):
            output_types.append("report")
        if any(term in content_lower for term in ["image", "chart", "graph", "visual"]):
            output_types.append("visual")

        template_complexity = "high" if len(output_types) >= 2 else "medium" if output_types else "low"

        return {
            "output_types": output_types,
            "template_complexity": template_complexity,
            "standardization_needed": len(output_types) > 0,
            "metadata_requirements": "metadata" in content_lower or "header" in content_lower
        }

    def _calculate_command_priority(self, analysis: Dict[str, Any]) -> str:
        """Calculate deployment priority for command"""

        priority_score = 0

        # Complexity weighting
        if analysis["complexity"] == "high":
            priority_score += 3
        elif analysis["complexity"] == "medium":
            priority_score += 2
        else:
            priority_score += 1

        # Command type weighting
        high_priority_types = ["analysis", "trading", "development"]
        if analysis["command_type"] in high_priority_types:
            priority_score += 2

        # Dependency weighting
        priority_score += len(analysis["dependencies"])

        # Evaluation complexity weighting
        eval_complexity = analysis["evaluation_requirements"]["complexity"]
        if eval_complexity == "comprehensive":
            priority_score += 2
        elif eval_complexity == "standard":
            priority_score += 1

        # Convert score to priority
        if priority_score >= 7:
            return "high"
        elif priority_score >= 4:
            return "medium"
        else:
            return "low"

    def _categorize_commands(self, remaining_commands: Dict[str, Any]) -> Dict[str, List[str]]:
        """Categorize commands by deployment strategy"""

        categories = {
            "high_priority": [],
            "medium_priority": [],
            "low_priority": [],
            "complex_analysis": [],
            "content_management": [],
            "development_tools": [],
            "trading_utilities": [],
            "business_management": []
        }

        for cmd_name, cmd_info in remaining_commands.items():
            # Priority categories
            priority = cmd_info.get("deployment_priority", "medium")
            categories[f"{priority}_priority"].append(cmd_name)

            # Type categories
            cmd_type = cmd_info.get("command_type", "utility")
            if cmd_type == "analysis":
                categories["complex_analysis"].append(cmd_name)
            elif cmd_type == "content":
                categories["content_management"].append(cmd_name)
            elif cmd_type == "development":
                categories["development_tools"].append(cmd_name)
            elif cmd_type == "trading":
                categories["trading_utilities"].append(cmd_name)
            elif cmd_type == "management":
                categories["business_management"].append(cmd_name)

        return categories

    def _calculate_deployment_priority(self, remaining_commands: Dict[str, Any]) -> List[str]:
        """Calculate optimal deployment order"""

        # Sort commands by priority score and dependencies
        command_priorities = []

        for cmd_name, cmd_info in remaining_commands.items():
            priority = cmd_info.get("deployment_priority", "medium")
            complexity = cmd_info.get("complexity", "medium")
            dependencies = len(cmd_info.get("dependencies", []))

            # Calculate deployment score
            score = 0
            if priority == "high":
                score += 10
            elif priority == "medium":
                score += 5
            else:
                score += 1

            if complexity == "high":
                score += 5
            elif complexity == "medium":
                score += 3
            else:
                score += 1

            score += dependencies

            command_priorities.append((cmd_name, score))

        # Sort by score (highest first)
        command_priorities.sort(key=lambda x: x[1], reverse=True)

        return [cmd_name for cmd_name, _ in command_priorities]

    def save_catalog(self, catalog: Dict[str, Any]) -> Path:
        """Save command catalog to file"""

        catalog_path = self.workspace_path / "framework" / "phase4_command_catalog.json"
        catalog_path.parent.mkdir(parents=True, exist_ok=True)

        with open(catalog_path, 'w') as f:
            json.dump(catalog, f, indent=2, default=str)

        return catalog_path

def main():
    """Run command cataloging for Phase 4"""
    print("🔍 PHASE 4 COMMAND CATALOG")
    print("Identifying commands for Universal Evaluation deployment")
    print("=" * 60)

    cataloger = Phase4CommandCatalog()
    catalog = cataloger.catalog_all_commands()

    print(f"\n📊 COMMAND ANALYSIS SUMMARY:")
    print(f"Total Commands: {catalog['total_commands']}")
    print(f"Already Integrated: {len(catalog['integrated_commands'])}")
    print(f"Legacy Commands: {len(catalog['legacy_commands'])}")
    print(f"Phase 4 Target Commands: {catalog['phase4_scope']['target_commands']}")

    print(f"\n🎯 DEPLOYMENT PRIORITIES:")
    deployment_order = catalog['phase4_scope']['deployment_priority']
    for i, cmd in enumerate(deployment_order[:5], 1):
        cmd_info = catalog['remaining_commands'][cmd]
        print(f"   {i}. {cmd} ({cmd_info['complexity']} complexity, {cmd_info['command_type']} type)")

    print(f"\n📋 COMMAND CATEGORIES:")
    categories = catalog['categorized_deployment']
    for category, commands in categories.items():
        if commands:
            print(f"   {category}: {len(commands)} commands")

    # Save catalog
    catalog_file = cataloger.save_catalog(catalog)
    print(f"\n💾 Catalog saved: {catalog_file}")

    return catalog

if __name__ == "__main__":
    main()
