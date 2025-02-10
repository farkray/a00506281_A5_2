#!/usr/bin/env python3
"""
Author: Dr. Farid Krayem Pineda
ID: A00506281
Date: February 2025
"""

import json
import sys
import time
from typing import Dict, List, Union, Tuple


def load_json_file(filename: str) -> Union[Dict, List]:
    """Load and parse a JSON file.

    Args:
        filename: Path to the JSON file

    Returns:
        Parsed JSON content as dict or list

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{filename}': {str(e)}")
        sys.exit(1)


def compute_sale_cost(
        sale: Dict,
        price_catalogue: Dict) -> Tuple[float, List[str]]:
    """Compute the total cost for a single sale.

    Args:
        sale: Dictionary containing the sale information
        price_catalogue: Dictionary containing product prices

    Returns:
        Tuple containing:
            - Total cost of the sale
            - List of error messages if any
    """
    total_cost = 0
    errors = []

    for item in sale.get('items', []):
        product_name = item.get('product')
        quantity = item.get('quantity', 0)

        if not product_name or not quantity:
            errors.append(
                f"Invalid item in sale {sale.get('id', 'Unknown')}: "
                f"Missing product name or quantity"
            )
            continue

        if product_name not in price_catalogue:
            errors.append(
                f"Product '{product_name}' not found in price catalogue"
            )
            continue

        try:
            price = float(price_catalogue[product_name])
            total_cost += price * quantity
        except (ValueError, TypeError):
            errors.append(
                f"Invalid price for product '{product_name}' "
                f"in price catalogue"
            )

    return total_cost, errors


def write_results(
        total_cost: float,
        execution_time: float,
        errors: List[str]) -> None:
    """Write results to both console and file.

    Args:
        total_cost: Total cost of all sales
        execution_time: Time taken to execute the program
        errors: List of errors encountered during execution
    """
    if errors:
        results = [
            "=== Sales Computation Results ===",
            f"Total Cost: ${total_cost:.2f}",
            f"Execution Time: {execution_time:.3f} seconds",
            "\nErrors encountered during execution:"
        ] + errors
    else:
        results = [
            "=== Sales Computation Results ===",
            f"Total Cost: ${total_cost:.2f}",
            f"Execution Time: {execution_time:.3f} seconds",
            "\nNo errors encountered during execution."
        ]

    print("\n".join(results))

    with open('SalesResults.txt', 'w', encoding='utf-8') as file:
        file.write("\n".join(results))


def main() -> None:
    """Main program execution."""
    if len(sys.argv) != 3:
        print(
            "Usage: python computeSales.py "
            "priceCatalogue.json salesRecord.json")
        sys.exit(1)

    start_time = time.time()

    price_catalogue = load_json_file(sys.argv[1])
    sales_record = load_json_file(sys.argv[2])

    total_cost = 0
    all_errors = []

    if not isinstance(sales_record, list):
        print("Error: Sales record must be a list of sales")
        sys.exit(1)

    for sale in sales_record:
        sale_cost, errors = compute_sale_cost(sale, price_catalogue)
        total_cost += sale_cost
        all_errors.extend(errors)

    execution_time = time.time() - start_time

    write_results(total_cost, execution_time, all_errors)


if __name__ == "__main__":
    main()
