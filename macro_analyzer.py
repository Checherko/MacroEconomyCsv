#!/usr/bin/env python3
"""
Macro Economic Data Analyzer

A script for processing CSV files with macroeconomic data and generating reports.
"""

import argparse
import csv
import sys
from collections import defaultdict
from typing import List, Dict, Any, Callable
from tabulate import tabulate


def read_csv_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Read and combine data from multiple CSV files.
    
    Args:
        file_paths: List of CSV file paths
        
    Returns:
        List of dictionaries containing economic data
    """
    data = []
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert numeric values
                    try:
                        row['gdp'] = float(row['gdp'])
                        row['year'] = int(row['year'])
                        row['gdp_growth'] = float(row['gdp_growth'])
                        row['inflation'] = float(row['inflation'])
                        row['unemployment'] = float(row['unemployment'])
                        row['population'] = int(row['population'])
                    except (ValueError, KeyError):
                        continue
                    data.append(row)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
            sys.exit(1)
    
    return data


def calculate_average_gdp(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculate average GDP by country.
    
    Args:
        data: List of economic data dictionaries
        
    Returns:
        List of dictionaries with country and average GDP, sorted by GDP descending
    """
    gdp_by_country = defaultdict(list)
    
    for row in data:
        country = row['country']
        gdp_by_country[country].append(row['gdp'])
    
    result = []
    for country, gdp_values in gdp_by_country.items():
        avg_gdp = sum(gdp_values) / len(gdp_values)
        result.append({
            'country': country,
            'average_gdp': round(avg_gdp, 2)
        })
    
    # Sort by average GDP descending
    result.sort(key=lambda x: x['average_gdp'], reverse=True)
    return result


# Registry of available reports
REPORTS = {
    'average-gdp': calculate_average_gdp,
}


def generate_report(data: List[Dict[str, Any]], report_type: str) -> List[Dict[str, Any]]:
    """
    Generate a specific type of report.
    
    Args:
        data: Economic data
        report_type: Type of report to generate
        
    Returns:
        Report data
    """
    if report_type not in REPORTS:
        available = ', '.join(REPORTS.keys())
        print(f"Error: Unknown report type '{report_type}'. Available: {available}", file=sys.stderr)
        sys.exit(1)
    
    return REPORTS[report_type](data)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Analyze macroeconomic data from CSV files'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='CSV files with economic data'
    )
    parser.add_argument(
        '--report',
        required=True,
        choices=list(REPORTS.keys()),
        help='Type of report to generate'
    )
    
    args = parser.parse_args()
    
    # Read data from files
    data = read_csv_files(args.files)
    
    if not data:
        print("No data found in the provided files.", file=sys.stderr)
        sys.exit(1)
    
    # Generate report
    report_data = generate_report(data, args.report)
    
    # Display results
    if args.report == 'average-gdp':
        headers = ['Country', 'Average GDP']
        rows = [[item['country'], item['average_gdp']] for item in report_data]
        print(tabulate(rows, headers=headers, tablefmt='grid'))


if __name__ == '__main__':
    main()
