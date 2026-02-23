#!/usr/bin/env python3
"""
Demonstration script for macro_analyzer.py
"""

import subprocess
import sys

def run_demo():
    """Run demonstration of the macro analyzer."""
    
    print("=== Macro Economic Data Analyzer Demo ===\n")
    
    # Demo 1: Single file
    print("1. Analyzing single file (economic1.csv):")
    print("Command: python macro_analyzer.py --files economic1.csv --report average-gdp")
    print("-" * 60)
    subprocess.run([
        sys.executable, "macro_analyzer.py", 
        "--files", "economic1.csv", 
        "--report", "average-gdp"
    ])
    print()
    
    # Demo 2: Multiple files
    print("2. Analyzing multiple files (economic1.csv + economic2.csv):")
    print("Command: python macro_analyzer.py --files economic1.csv economic2.csv --report average-gdp")
    print("-" * 60)
    subprocess.run([
        sys.executable, "macro_analyzer.py", 
        "--files", "economic1.csv", "economic2.csv", 
        "--report", "average-gdp"
    ])
    print()
    
    # Demo 3: Help
    print("3. Help information:")
    print("Command: python macro_analyzer.py --help")
    print("-" * 60)
    subprocess.run([sys.executable, "macro_analyzer.py", "--help"])

if __name__ == "__main__":
    run_demo()
