#!/usr/bin/env python3
"""
StockX Price Checker - Command line tool to fetch pricing data for shoes on StockX.
"""
import argparse
import sys
from typing import Tuple
from stockx_api import StockXAPI

def validate_size(size: str) -> float:
    """
    Validate the shoe size input.
    
    Args:
        size: String representation of shoe size
        
    Returns:
        Float representation of valid shoe size
        
    Raises:
        ValueError: If size is invalid
    """
    try:
        size_float = float(size)
        if size_float < 3.5 or size_float > 18:
            raise ValueError
        return size_float
    except ValueError:
        raise ValueError("Invalid size. Please enter a valid shoe size (3.5-18)")

def format_price(price: float) -> str:
    """
    Format price with 2 decimal places and dollar sign.
    
    Args:
        price: Float price value
        
    Returns:
        Formatted price string
    """
    return f"${price:.2f}"

def get_prices(shoe_name: str, size: float) -> Tuple[float, float, float]:
    """
    Get pricing data from StockX API.
    
    Args:
        shoe_name: Name of the shoe
        size: Shoe size
        
    Returns:
        Tuple of (bid, ask, payout) prices
    """
    api = StockXAPI()  # Will add credentials here later
    return api.get_price_data(shoe_name, size)

def main():
    """Main entry point for the price checker."""
    parser = argparse.ArgumentParser(description="Check StockX prices for shoes")
    parser.add_argument("shoe_name", help="Name of the shoe")
    parser.add_argument("size", help="Shoe size (US)")
    
    args = parser.parse_args()

    try:
        # Validate size input
        size = validate_size(args.size)
        
        # Get pricing data
        bid, ask, payout = get_prices(args.shoe_name, size)
        
        # Display results
        print("\nStockX Pricing Data")
        print("-" * 20)
        print(f"Shoe: {args.shoe_name}")
        print(f"Size: {size}")
        print(f"Highest Bid: {format_price(bid)}")
        print(f"Lowest Ask: {format_price(ask)}")
        print(f"Payout: {format_price(payout)}")
        
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
