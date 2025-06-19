#!/usr/bin/env python3
"""
FReview - Flask Project Review Tool

This is an alternative entry point for the freview CLI.
The main entry point is through the CLI module.
"""

from freview.cli import app

def main():
    """Main entry point for freview."""
    app()

if __name__ == "__main__":
    main()
