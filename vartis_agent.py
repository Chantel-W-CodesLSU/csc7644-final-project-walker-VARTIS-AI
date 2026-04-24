"""
vartis_agent.py

Main entry point for Vartis Care AI.
CSC 7644: Applied LLM Development - Final Project
Author: Chantel Walker

This module handles command-line interaction and coordinates
the eligibility extraction pipeline for healthcare patient advocacy.
"""

import argparse
import json
from extractor import extract_info


def parse_arguments():
    """
    Parse command-line arguments for the Vartis Care AI agent.

    Returns:
        argparse.Namespace: Parsed arguments containing mode and input path.
    """
    parser = argparse.ArgumentParser(
        description="Vartis Care AI - Patient Eligibility Extraction Tool"
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["extract"],
        help="Operation mode: extract to process patient intake data"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the patient intake text file"
    )
    return parser.parse_args()


def main():
    """
    Main function to run the Vartis Care AI agent.

    Reads a patient intake file, extracts eligibility markers,
    and prints matched resources as formatted JSON.
    """
    args = parse_arguments()

    if args.mode == "extract":
        with open(args.input, "r") as f:
            text = f.read()

        output = extract_info(text)

        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()