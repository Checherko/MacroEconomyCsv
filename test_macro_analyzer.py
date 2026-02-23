#!/usr/bin/env python3
"""
Tests for macro_analyzer.py
"""

import pytest
import tempfile
import os
import csv
from unittest.mock import patch
from io import StringIO
import sys

from macro_analyzer import (
    read_csv_files,
    calculate_average_gdp,
    generate_report,
    REPORTS
)


def create_test_csv(data, filename):
    """Create a temporary CSV file with test data."""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def test_read_csv_files_single():
    """Test reading a single CSV file."""
    test_data = [
        {
            'country': 'Test Country',
            'year': '2023',
            'gdp': '1000',
            'gdp_growth': '2.5',
            'inflation': '3.0',
            'unemployment': '5.0',
            'population': '10',
            'continent': 'Test Continent'
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        filename = f.name
    
    try:
        create_test_csv(test_data, filename)
        result = read_csv_files([filename])
        
        assert len(result) == 1
        assert result[0]['country'] == 'Test Country'
        assert result[0]['gdp'] == 1000.0
        assert result[0]['year'] == 2023
    finally:
        os.unlink(filename)


def test_read_csv_files_multiple():
    """Test reading multiple CSV files."""
    test_data1 = [
        {
            'country': 'Country A',
            'year': '2023',
            'gdp': '1000',
            'gdp_growth': '2.5',
            'inflation': '3.0',
            'unemployment': '5.0',
            'population': '10',
            'continent': 'Continent A'
        }
    ]
    
    test_data2 = [
        {
            'country': 'Country B',
            'year': '2023',
            'gdp': '2000',
            'gdp_growth': '3.0',
            'inflation': '2.5',
            'unemployment': '4.0',
            'population': '20',
            'continent': 'Continent B'
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f1:
        filename1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f2:
        filename2 = f2.name
    
    try:
        create_test_csv(test_data1, filename1)
        create_test_csv(test_data2, filename2)
        result = read_csv_files([filename1, filename2])
        
        assert len(result) == 2
        assert result[0]['country'] == 'Country A'
        assert result[1]['country'] == 'Country B'
    finally:
        os.unlink(filename1)
        os.unlink(filename2)


def test_read_csv_file_not_found():
    """Test handling of non-existent file."""
    with pytest.raises(SystemExit):
        read_csv_files(['nonexistent.csv'])


def test_calculate_average_gdp():
    """Test average GDP calculation."""
    test_data = [
        {'country': 'Country A', 'gdp': 1000},
        {'country': 'Country A', 'gdp': 2000},
        {'country': 'Country B', 'gdp': 3000},
        {'country': 'Country B', 'gdp': 4000},
    ]
    
    result = calculate_average_gdp(test_data)
    
    assert len(result) == 2
    assert result[0]['country'] == 'Country B'  # Higher average GDP first
    assert result[0]['average_gdp'] == 3500.0
    assert result[1]['country'] == 'Country A'
    assert result[1]['average_gdp'] == 1500.0


def test_calculate_average_gdp_single_entry():
    """Test average GDP calculation with single entry per country."""
    test_data = [
        {'country': 'Country A', 'gdp': 1000},
        {'country': 'Country B', 'gdp': 2000},
    ]
    
    result = calculate_average_gdp(test_data)
    
    assert len(result) == 2
    assert result[0]['country'] == 'Country B'  # Higher GDP first
    assert result[0]['average_gdp'] == 2000.0
    assert result[1]['country'] == 'Country A'
    assert result[1]['average_gdp'] == 1000.0


def test_generate_report_valid():
    """Test generating a valid report."""
    test_data = [
        {'country': 'Country A', 'gdp': 1000},
        {'country': 'Country B', 'gdp': 2000},
    ]
    
    result = generate_report(test_data, 'average-gdp')
    
    assert len(result) == 2
    assert 'country' in result[0]
    assert 'average_gdp' in result[0]


def test_generate_report_invalid():
    """Test generating an invalid report type."""
    test_data = [{'country': 'Country A', 'gdp': 1000}]
    
    with pytest.raises(SystemExit):
        generate_report(test_data, 'invalid-report')


def test_reports_registry():
    """Test that reports registry contains expected reports."""
    assert 'average-gdp' in REPORTS
    assert callable(REPORTS['average-gdp'])


def test_main_function_integration():
    """Test main function integration with mocked arguments."""
    test_data = [
        {
            'country': 'Country A',
            'year': '2023',
            'gdp': '1000',
            'gdp_growth': '2.5',
            'inflation': '3.0',
            'unemployment': '5.0',
            'population': '10',
            'continent': 'Continent A'
        },
        {
            'country': 'Country A',
            'year': '2022',
            'gdp': '2000',
            'gdp_growth': '3.0',
            'inflation': '2.5',
            'unemployment': '4.0',
            'population': '10',
            'continent': 'Continent A'
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        filename = f.name
    
    try:
        create_test_csv(test_data, filename)
        
        # Mock sys.argv
        test_args = [
            'macro_analyzer.py',
            '--files', filename,
            '--report', 'average-gdp'
        ]
        
        with patch.object(sys, 'argv', test_args):
            # Capture stdout
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                from macro_analyzer import main
                main()
            
            output = captured_output.getvalue()
            assert 'Country A' in output
            assert '1500' in output  # Average of 1000 and 2000
            
    finally:
        os.unlink(filename)
