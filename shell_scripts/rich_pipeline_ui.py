#!/usr/bin/env python3
"""
Rich Terminal UI for Fundamental Analysis Pipeline

This module provides enhanced terminal output for the fundamental_analysis_pipeline.sh
script using the Rich library for beautiful, interactive terminal experiences.
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.text import Text
    from rich.markdown import Markdown
    from rich.rule import Rule
    from rich.columns import Columns
    from rich.align import Align
    from rich.layout import Layout
    from rich.live import Live
    from rich.prompt import Confirm, Prompt
    import rich.box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Global console instance
console = Console() if RICH_AVAILABLE else None

class PipelineUI:
    """Rich UI controller for the fundamental analysis pipeline"""

    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.phases = {
            1: {"name": "Discovery", "status": "pending", "start_time": None, "end_time": None},
            2: {"name": "Analysis", "status": "pending", "start_time": None, "end_time": None},
            3: {"name": "Synthesis", "status": "pending", "start_time": None, "end_time": None},
            4: {"name": "Validation", "status": "pending", "start_time": None, "end_time": None}
        }
        self.current_phase = 0
        self.ticker = ""
        self.execution_id = ""

    def display_header(self, ticker: str, analysis_date: str, execution_id: str):
        """Display a rich header for the pipeline execution"""
        if not RICH_AVAILABLE:
            print(f"=== FUNDAMENTAL ANALYSIS PIPELINE ===")
            print(f"Ticker: {ticker} | Date: {analysis_date} | ID: {execution_id}")
            return

        self.ticker = ticker
        self.execution_id = execution_id

        header_table = Table.grid(expand=True)
        header_table.add_column(justify="left")
        header_table.add_column(justify="center")
        header_table.add_column(justify="right")

        header_table.add_row(
            f"[bold blue]📊 Ticker:[/bold blue] [green]{ticker}[/green]",
            f"[bold blue]📅 Date:[/bold blue] [yellow]{analysis_date}[/yellow]",
            f"[bold blue]🆔 ID:[/bold blue] [dim]{execution_id[:12]}...[/dim]"
        )

        panel = Panel(
            header_table,
            title="[bold cyan]🔍 FUNDAMENTAL ANALYSIS PIPELINE[/bold cyan]",
            subtitle="[dim]Claude Code Enhanced Terminal Output[/dim]",
            border_style="cyan",
            box=rich.box.ROUNDED
        )

        self.console.print()
        self.console.print(panel)
        self.console.print()

    def display_phase_progress(self, phase: int, status: str, message: str = ""):
        """Update and display the current phase progress"""
        if not RICH_AVAILABLE:
            print(f"Phase {phase}/4: {self.phases[phase]['name']} - {status.upper()}")
            if message:
                print(f"  {message}")
            return

        if phase in self.phases:
            self.phases[phase]["status"] = status
            if status == "running":
                self.phases[phase]["start_time"] = datetime.now()
            elif status == "completed":
                self.phases[phase]["end_time"] = datetime.now()

        self.current_phase = phase

        # Create progress visualization
        progress_table = Table(show_header=False, expand=True, box=None)
        progress_table.add_column("Phase", style="bold")
        progress_table.add_column("Status", justify="center")
        progress_table.add_column("Time", justify="right", style="dim")

        for phase_num, phase_data in self.phases.items():
            phase_name = phase_data["name"]
            phase_status = phase_data["status"]

            # Status icons and colors
            if phase_status == "completed":
                status_text = "[green]✅ Completed[/green]"
            elif phase_status == "running":
                status_text = "[yellow]🔄 Running[/yellow]"
            elif phase_status == "failed":
                status_text = "[red]❌ Failed[/red]"
            else:
                status_text = "[dim]⏳ Pending[/dim]"

            # Calculate duration
            duration = ""
            if phase_data["start_time"]:
                end_time = phase_data["end_time"] or datetime.now()
                duration_seconds = (end_time - phase_data["start_time"]).total_seconds()
                duration = f"{duration_seconds:.1f}s"

            progress_table.add_row(
                f"[bold]{phase_num}. {phase_name}[/bold]",
                status_text,
                duration
            )

        panel = Panel(
            progress_table,
            title="[bold cyan]📋 Pipeline Progress[/bold cyan]",
            border_style="blue",
            box=rich.box.ROUNDED
        )

        self.console.clear()
        self.display_header(self.ticker, datetime.now().strftime("%Y%m%d"), self.execution_id)
        self.console.print(panel)

        if message:
            self.console.print(f"[dim]ℹ️  {message}[/dim]")

        self.console.print()

    def display_confidence_check(self, confidence_score: float, threshold: float, passed: bool):
        """Display confidence threshold checking results"""
        if not RICH_AVAILABLE:
            status = "PASSED" if passed else "FAILED"
            print(f"Confidence Check: {confidence_score:.1f}/10.0 (threshold: {threshold}) - {status}")
            return

        # Create confidence visualization
        confidence_table = Table(show_header=False, expand=True)
        confidence_table.add_column("Metric", style="bold")
        confidence_table.add_column("Value", justify="center")
        confidence_table.add_column("Status", justify="right")

        confidence_table.add_row(
            "Confidence Score",
            f"[bold]{confidence_score:.1f}/10.0[/bold]",
            f"[green]✅ Above Threshold[/green]" if passed else f"[red]❌ Below Threshold[/red]"
        )

        confidence_table.add_row(
            "Required Threshold",
            f"[dim]{threshold:.1f}/10.0[/dim]",
            ""
        )

        border_color = "green" if passed else "red"
        title_icon = "✅" if passed else "❌"

        panel = Panel(
            confidence_table,
            title=f"[bold]{title_icon} Confidence Assessment[/bold]",
            border_style=border_color,
            box=rich.box.ROUNDED
        )

        self.console.print(panel)

    def display_execution_summary(self, summary_data: Dict[str, Any]):
        """Display rich execution summary with file verification"""
        if not RICH_AVAILABLE:
            self._display_plain_summary(summary_data)
            return

        metadata = summary_data.get("execution_metadata", {})
        output_files = summary_data.get("output_files", {})
        file_verification = summary_data.get("file_verification", {})

        # Metadata panel
        metadata_table = Table(show_header=False, expand=True)
        metadata_table.add_column("Property", style="bold cyan")
        metadata_table.add_column("Value", style="white")

        metadata_table.add_row("Ticker Symbol", f"[green]{metadata.get('ticker', 'N/A')}[/green]")
        metadata_table.add_row("Analysis Date", f"[yellow]{metadata.get('analysis_date', 'N/A')}[/yellow]")
        metadata_table.add_row("Execution ID", f"[dim]{metadata.get('execution_id', 'N/A')}[/dim]")
        metadata_table.add_row("Confidence Threshold", f"{metadata.get('confidence_threshold', 'N/A')}")
        metadata_table.add_row("Retry Attempts", f"{metadata.get('retry_attempts_used', 0)}/{metadata.get('retry_attempts_used', 0)}")

        metadata_panel = Panel(
            metadata_table,
            title="[bold cyan]📊 Execution Metadata[/bold cyan]",
            border_style="cyan",
            box=rich.box.ROUNDED
        )

        # File verification panel
        files_table = Table(expand=True)
        files_table.add_column("Phase", style="bold")
        files_table.add_column("Status", justify="center")
        files_table.add_column("Size", justify="right")
        files_table.add_column("Modified", justify="right", style="dim")

        for phase, file_path in output_files.items():
            verification = file_verification.get(phase, {})

            if verification.get("exists", False):
                status_text = "[green]✅ Created[/green]"
                size_kb = verification.get("size_bytes", 0) / 1024
                size_text = f"{size_kb:.1f}KB" if size_kb > 0 else "0KB"
                modified_time = verification.get("last_modified", "")
                if modified_time:
                    try:
                        dt = datetime.fromisoformat(modified_time.replace('Z', '+00:00'))
                        modified_text = dt.strftime("%H:%M:%S")
                    except:
                        modified_text = "Unknown"
                else:
                    modified_text = "Unknown"
            else:
                status_text = "[red]❌ Missing[/red]"
                size_text = "0KB"
                modified_text = "N/A"

            files_table.add_row(
                phase.capitalize(),
                status_text,
                size_text,
                modified_text
            )

        files_panel = Panel(
            files_table,
            title="[bold green]📁 Output Files[/bold green]",
            border_style="green",
            box=rich.box.ROUNDED
        )

        # Display panels
        self.console.print()
        self.console.print(Rule("[bold cyan]🎉 EXECUTION COMPLETE[/bold cyan]", style="cyan"))
        self.console.print()

        # Use columns for side-by-side display
        self.console.print(Columns([metadata_panel, files_panel], equal=True))

        self.console.print()
        self.console.print("[dim]💡 Check the log file for detailed execution information[/dim]")
        self.console.print()

    def _display_plain_summary(self, summary_data: Dict[str, Any]):
        """Fallback plain text summary display"""
        print("\n" + "="*60)
        print("EXECUTION SUMMARY")
        print("="*60)

        metadata = summary_data.get("execution_metadata", {})
        print(f"Ticker: {metadata.get('ticker', 'N/A')}")
        print(f"Date: {metadata.get('analysis_date', 'N/A')}")
        print(f"Execution ID: {metadata.get('execution_id', 'N/A')}")
        print(f"Confidence Threshold: {metadata.get('confidence_threshold', 'N/A')}")

        print("\nOutput Files:")
        file_verification = summary_data.get("file_verification", {})
        for phase, verification in file_verification.items():
            status = "✓" if verification.get("exists", False) else "✗"
            size_kb = verification.get("size_bytes", 0) / 1024
            print(f"  {status} {phase.capitalize()}: {size_kb:.1f}KB")

        print("="*60)

    def display_error(self, error_message: str, error_code: int = 1, details: str = ""):
        """Display rich error formatting"""
        if not RICH_AVAILABLE:
            print(f"ERROR ({error_code}): {error_message}", file=sys.stderr)
            if details:
                print(f"Details: {details}", file=sys.stderr)
            return

        error_content = f"[bold red]Error Code:[/bold red] {error_code}\n"
        error_content += f"[bold red]Message:[/bold red] {error_message}"

        if details:
            error_content += f"\n[bold red]Details:[/bold red] {details}"

        panel = Panel(
            error_content,
            title="[bold red]🚨 PIPELINE ERROR[/bold red]",
            border_style="red",
            box=rich.box.ROUNDED
        )

        self.console.print()
        self.console.print(panel)
        self.console.print()

    def prompt_confirmation(self, ticker: str, analysis_date: str) -> bool:
        """Interactive confirmation prompt"""
        if not RICH_AVAILABLE:
            response = input(f"Execute pipeline for {ticker} on {analysis_date}? [y/N]: ")
            return response.lower().startswith('y')

        self.console.print()
        self.console.print(f"[bold]About to execute fundamental analysis pipeline:[/bold]")
        self.console.print(f"📊 Ticker: [green]{ticker}[/green]")
        self.console.print(f"📅 Date: [yellow]{analysis_date}[/yellow]")
        self.console.print()

        return Confirm.ask("[bold]Proceed with execution?[/bold]", default=False)

def main():
    """Main entry point for command-line usage"""
    parser = argparse.ArgumentParser(description="Rich UI for Fundamental Analysis Pipeline")
    parser.add_argument("command", choices=[
        "header", "phase", "confidence", "summary", "error", "confirm"
    ], help="UI command to execute")

    # Common arguments
    parser.add_argument("--ticker", help="Stock ticker symbol")
    parser.add_argument("--date", help="Analysis date")
    parser.add_argument("--execution-id", help="Execution ID")

    # Phase-specific arguments
    parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4], help="Phase number")
    parser.add_argument("--status", choices=["pending", "running", "completed", "failed"], help="Phase status")
    parser.add_argument("--message", help="Additional message")

    # Confidence arguments
    parser.add_argument("--confidence-score", type=float, help="Confidence score")
    parser.add_argument("--threshold", type=float, help="Confidence threshold")
    parser.add_argument("--passed", action="store_true", help="Confidence check passed")

    # Summary arguments
    parser.add_argument("--summary-file", help="Path to summary JSON file")

    # Error arguments
    parser.add_argument("--error-message", help="Error message")
    parser.add_argument("--error-code", type=int, default=1, help="Error code")
    parser.add_argument("--error-details", help="Error details")

    args = parser.parse_args()

    ui = PipelineUI()

    if args.command == "header":
        ui.display_header(
            args.ticker or "UNKNOWN",
            args.date or datetime.now().strftime("%Y%m%d"),
            args.execution_id or "unknown"
        )

    elif args.command == "phase":
        if args.phase and args.status:
            ui.display_phase_progress(args.phase, args.status, args.message or "")
        else:
            print("Error: --phase and --status required for phase command", file=sys.stderr)
            sys.exit(1)

    elif args.command == "confidence":
        if args.confidence_score is not None and args.threshold is not None:
            ui.display_confidence_check(args.confidence_score, args.threshold, args.passed)
        else:
            print("Error: --confidence-score and --threshold required for confidence command", file=sys.stderr)
            sys.exit(1)

    elif args.command == "summary":
        if args.summary_file and Path(args.summary_file).exists():
            with open(args.summary_file, 'r') as f:
                summary_data = json.load(f)
            ui.display_execution_summary(summary_data)
        else:
            print("Error: --summary-file required and must exist for summary command", file=sys.stderr)
            sys.exit(1)

    elif args.command == "error":
        if args.error_message:
            ui.display_error(args.error_message, args.error_code, args.error_details or "")
        else:
            print("Error: --error-message required for error command", file=sys.stderr)
            sys.exit(1)

    elif args.command == "confirm":
        if args.ticker and args.date:
            confirmed = ui.prompt_confirmation(args.ticker, args.date)
            sys.exit(0 if confirmed else 1)
        else:
            print("Error: --ticker and --date required for confirm command", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
