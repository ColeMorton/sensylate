#!/usr/bin/env python3
"""
Team-Workspace Content Lifecycle Management - Conflict Detection System

Automated detection of duplicate analyses, contradictory status reports,
and temporal inconsistencies in team-workspace content.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime, timedelta
import hashlib

class ConflictDetector:
    """Detects and reports conflicts in team-workspace content."""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.registry_path = self.workspace_path / "coordination" / "topic-registry.yaml"
        self.conflicts = []

    def detect_all_conflicts(self) -> Dict[str, List[Dict]]:
        """Run comprehensive conflict detection across all content."""
        conflicts = {
            "duplications": self.detect_duplicate_content(),
            "contradictions": self.detect_status_contradictions(),
            "temporal_issues": self.detect_temporal_inconsistencies(),
            "orphaned_content": self.detect_orphaned_content()
        }

        return conflicts

    def detect_duplicate_content(self) -> List[Dict]:
        """Detect files with similar content or overlapping topics."""
        duplicates = []
        file_signatures = {}

        # Scan all output files
        outputs_path = self.workspace_path / "commands"
        for command_dir in outputs_path.iterdir():
            if not command_dir.is_dir():
                continue

            outputs_dir = command_dir / "outputs"
            if not outputs_dir.exists():
                continue

            for file_path in outputs_dir.glob("*.md"):
                content = self._read_file_safe(file_path)
                if not content:
                    continue

                # Create content signature for similarity detection
                signature = self._create_content_signature(content)
                title_keywords = self._extract_title_keywords(content)

                # Check for similar content
                for existing_file, existing_data in file_signatures.items():
                    similarity = self._calculate_similarity(signature, existing_data["signature"])
                    keyword_overlap = len(title_keywords & existing_data["keywords"])

                    if similarity > 0.7 or keyword_overlap >= 3:
                        duplicates.append({
                            "type": "content_duplication",
                            "files": [str(file_path), existing_file],
                            "similarity_score": similarity,
                            "keyword_overlap": keyword_overlap,
                            "severity": "high" if similarity > 0.8 else "medium"
                        })

                file_signatures[str(file_path)] = {
                    "signature": signature,
                    "keywords": title_keywords
                }

        return duplicates

    def detect_status_contradictions(self) -> List[Dict]:
        """Detect contradictory status reports for same projects/topics."""
        contradictions = []

        # Load topic registry to check for known conflicts
        registry = self._load_registry()
        if not registry:
            return contradictions

        for topic_name, topic_data in registry.get("topics", {}).items():
            if topic_data.get("conflicts_detected"):
                related_files = topic_data.get("related_files", [])
                if len(related_files) > 1:
                    # Analyze each file for status indicators
                    status_reports = []
                    for file_path in related_files:
                        full_path = Path(file_path)
                        if full_path.exists():
                            content = self._read_file_safe(full_path)
                            status = self._extract_status_indicators(content)
                            status_reports.append({
                                "file": str(full_path),
                                "status": status
                            })

                    # Check for contradictions
                    if len(status_reports) > 1:
                        unique_statuses = set(report["status"]["overall"] for report in status_reports if report["status"]["overall"])
                        if len(unique_statuses) > 1:
                            contradictions.append({
                                "type": "status_contradiction",
                                "topic": topic_name,
                                "conflicting_statuses": list(unique_statuses),
                                "files": [report["file"] for report in status_reports],
                                "severity": "high"
                            })

        return contradictions

    def detect_temporal_inconsistencies(self) -> List[Dict]:
        """Detect temporal issues like wrong dates or impossible timestamps."""
        temporal_issues = []

        outputs_path = self.workspace_path / "commands"
        for command_dir in outputs_path.iterdir():
            if not command_dir.is_dir():
                continue

            outputs_dir = command_dir / "outputs"
            if not outputs_dir.exists():
                continue

            for file_path in outputs_dir.glob("*.md"):
                content = self._read_file_safe(file_path)
                if not content:
                    continue

                # Extract dates from content and filename
                content_date = self._extract_content_date(content)
                filename_date = self._extract_filename_date(file_path.name)
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)

                # Check for impossible dates (future dates beyond reasonable threshold)
                now = datetime.now()
                if content_date and content_date > now + timedelta(days=1):
                    temporal_issues.append({
                        "type": "future_date",
                        "file": str(file_path),
                        "content_date": content_date.isoformat(),
                        "severity": "medium"
                    })

                # Check for date mismatches
                if content_date and filename_date:
                    if abs((content_date - filename_date).days) > 1:
                        temporal_issues.append({
                            "type": "date_mismatch",
                            "file": str(file_path),
                            "content_date": content_date.isoformat(),
                            "filename_date": filename_date.isoformat(),
                            "severity": "low"
                        })

                # Check for files claiming old dates but recently modified
                if content_date and content_date < now - timedelta(days=180):
                    if file_mtime > now - timedelta(days=7):
                        temporal_issues.append({
                            "type": "stale_date_recent_file",
                            "file": str(file_path),
                            "claimed_date": content_date.isoformat(),
                            "actual_modified": file_mtime.isoformat(),
                            "severity": "high"
                        })

        return temporal_issues

    def detect_orphaned_content(self) -> List[Dict]:
        """Detect content not tracked in topic registry."""
        orphaned = []

        registry = self._load_registry()
        if not registry:
            return orphaned

        tracked_files = set()
        for topic_data in registry.get("topics", {}).values():
            tracked_files.update(topic_data.get("related_files", []))

        # Find all actual output files
        actual_files = set()
        outputs_path = self.workspace_path / "commands"
        for command_dir in outputs_path.iterdir():
            if not command_dir.is_dir():
                continue

            outputs_dir = command_dir / "outputs"
            if not outputs_dir.exists():
                continue

            for file_path in outputs_dir.glob("*.md"):
                # Convert to relative path format used in registry
                try:
                    relative_path = str(file_path.relative_to(Path.cwd()))
                    actual_files.add(relative_path)
                except ValueError:
                    # Handle absolute/relative path mismatch
                    relative_path = str(file_path)
                    actual_files.add(relative_path)

        # Find orphaned files
        orphaned_files = actual_files - tracked_files
        for orphaned_file in orphaned_files:
            orphaned.append({
                "type": "orphaned_content",
                "file": orphaned_file,
                "severity": "low"
            })

        return orphaned

    def _read_file_safe(self, file_path: Path) -> Optional[str]:
        """Safely read file content."""
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception:
            return None

    def _load_registry(self) -> Optional[Dict]:
        """Load topic registry."""
        try:
            if self.registry_path.exists():
                return yaml.safe_load(self.registry_path.read_text())
        except Exception:
            pass
        return None

    def _create_content_signature(self, content: str) -> str:
        """Create signature for content similarity detection."""
        # Remove dates, timestamps, and variable content
        cleaned = re.sub(r'\d{4}-\d{2}-\d{2}', '', content)
        cleaned = re.sub(r'_Generated.*?_', '', cleaned)
        cleaned = re.sub(r'Phase \d+:', '', cleaned)

        # Extract key phrases and create hash
        words = re.findall(r'\b[a-zA-Z]{4,}\b', cleaned.lower())
        key_phrases = ' '.join(sorted(set(words)))
        return hashlib.md5(key_phrases.encode()).hexdigest()

    def _extract_title_keywords(self, content: str) -> Set[str]:
        """Extract keywords from title and headers."""
        keywords = set()

        # Extract from title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title_words = re.findall(r'\b[a-zA-Z]{3,}\b', title_match.group(1).lower())
            keywords.update(title_words)

        # Extract from H2 headers
        headers = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        for header in headers:
            header_words = re.findall(r'\b[a-zA-Z]{3,}\b', header.lower())
            keywords.update(header_words)

        return keywords

    def _calculate_similarity(self, sig1: str, sig2: str) -> float:
        """Calculate similarity between two content signatures."""
        if sig1 == sig2:
            return 1.0

        # Simple Hamming distance for hash comparison
        if len(sig1) != len(sig2):
            return 0.0

        matches = sum(c1 == c2 for c1, c2 in zip(sig1, sig2))
        return matches / len(sig1)

    def _extract_status_indicators(self, content: str) -> Dict[str, Optional[str]]:
        """Extract status indicators from content."""
        status = {"overall": None, "specific": []}

        # Look for common status patterns
        status_patterns = [
            (r'Status.*?:\s*(\w+)', "overall"),
            (r'Health Score.*?:\s*([A-F][+-]?)', "overall"),
            (r'(?:Complete|Completed|Done)', "completed"),
            (r'(?:Critical|P0|High Priority)', "critical"),
            (r'(?:In Progress|Ongoing)', "in_progress")
        ]

        for pattern, status_type in status_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                if status_type == "overall":
                    status["overall"] = matches[0]
                else:
                    status["specific"].append(status_type)

        return status

    def _extract_content_date(self, content: str) -> Optional[datetime]:
        """Extract date from content."""
        # Look for various date patterns
        date_patterns = [
            r'_Generated:\s*(\w+\s+\d{1,2},\s*\d{4})_',
            r'Date.*?:\s*(\d{4}-\d{2}-\d{2})',
            r'(\w+\s+\d{1,2},\s*\d{4})'
        ]

        for pattern in date_patterns:
            match = re.search(pattern, content)
            if match:
                try:
                    date_str = match.group(1)
                    # Try different date formats
                    for fmt in ['%B %d, %Y', '%Y-%m-%d', '%b %d, %Y']:
                        try:
                            return datetime.strptime(date_str, fmt)
                        except ValueError:
                            continue
                except Exception:
                    continue

        return None

    def _extract_filename_date(self, filename: str) -> Optional[datetime]:
        """Extract date from filename."""
        date_match = re.search(r'(\d{8})', filename)
        if date_match:
            try:
                return datetime.strptime(date_match.group(1), '%Y%m%d')
            except ValueError:
                pass

        return None

def main():
    """Run conflict detection and report results."""
    detector = ConflictDetector()
    conflicts = detector.detect_all_conflicts()

    print("Team-Workspace Conflict Detection Report")
    print("=" * 50)

    total_conflicts = sum(len(conflict_list) for conflict_list in conflicts.values())
    print(f"Total conflicts detected: {total_conflicts}")

    for conflict_type, conflict_list in conflicts.items():
        if conflict_list:
            print(f"\n{conflict_type.upper()}:")
            for i, conflict in enumerate(conflict_list, 1):
                print(f"  {i}. {conflict}")

    if total_conflicts == 0:
        print("\n✅ No conflicts detected in team-workspace content!")

if __name__ == "__main__":
    main()
