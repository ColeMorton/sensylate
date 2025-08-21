#!/usr/bin/env python3
"""
Generic stock data copy script - supports any ticker symbol
Usage: python copy_stock_data.py SYMBOL
Example: python copy_stock_data.py AAPL
         python copy_stock_data.py MSTR
"""

import pandas as pd
import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import json
import argparse


def fetch_and_copy_stock_data(symbol: str) -> bool:
    """Fetch 1 year of stock data for any symbol and copy to frontend directory"""
    
    # Define paths dynamically based on symbol
    project_root = Path(__file__).parent.parent
    frontend_csv_path = project_root / f"frontend/public/data/raw/stocks/{symbol}/daily.csv"
    
    # Check if data already exists in scripts directory (from pipeline)
    scripts_csv_path = project_root / f"scripts/data/raw/stocks/{symbol}/daily.csv"
    
    try:
        if scripts_csv_path.exists():
            print(f"Found existing processed data for {symbol}")
            # Read the existing processed data
            df = pd.read_csv(scripts_csv_path)
            print(f"Found existing processed data with {len(df)} rows")
        else:
            print(f"Fetching 1 year of {symbol} data...")
            # Use Yahoo Finance CLI to get 1 year of data for the specified symbol
            result = subprocess.run([
                sys.executable, "yahoo_finance_cli.py", "history", symbol, 
                "--period", "1y", "--env", "dev", "--output-format", "json"
            ], cwd=Path(__file__).parent, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error fetching {symbol} data: {result.stderr}")
                return False
                
            if not scripts_csv_path.exists():
                print(f"No {symbol} data found at {scripts_csv_path} after fetch")
                return False
                
            # Read the newly fetched data
            df = pd.read_csv(scripts_csv_path)
            print(f"Retrieved {len(df)} rows of data")
        
        # Ensure we have date column in the right format
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # Sort by date to ensure chronological order
        df = df.sort_values('date')
        
        # Ensure frontend directory exists
        frontend_csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to CSV
        df.to_csv(frontend_csv_path, index=False)
        
        print(f"Successfully copied {len(df)} rows of {symbol} data to {frontend_csv_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {symbol} data: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Copy stock data for any symbol to frontend")
    parser.add_argument("symbol", help="Stock symbol (e.g., AAPL, MSTR, TSLA)")
    
    args = parser.parse_args()
    symbol = args.symbol.upper()  # Ensure uppercase
    
    print(f"Starting data copy process for symbol: {symbol}")
    
    success = fetch_and_copy_stock_data(symbol)
    
    if success:
        print(f"✅ Successfully completed data copy for {symbol}")
    else:
        print(f"❌ Failed to copy data for {symbol}")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()