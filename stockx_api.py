"""
StockX API client module for fetching product pricing data.
"""
import requests
from typing import Dict, Tuple
import time

class StockXAPI:
    def __init__(self):
        """Initialize the StockX API client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://stockx.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://stockx.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Connection': 'keep-alive'
        })
        self.base_url = "https://api.stockx.com/v2"

    def _make_request(self, url: str, params: Dict = None, retries: int = 3) -> Dict:
        """
        Make a request with retry logic and proper error handling.
        
        Args:
            url: The URL to request
            params: Query parameters
            retries: Number of retry attempts
            
        Returns:
            Dict containing response data
            
        Raises:
            ValueError: If request fails after all retries
        """
        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    raise ValueError(f"Failed to fetch data: {str(e)}")
                time.sleep(1)  # Wait before retrying

    def get_product_info(self, product_name: str) -> Dict:
        """
        Search for a product on StockX.
        
        Args:
            product_name: Name of the shoe to search for
            
        Returns:
            Dict containing product information
        """
        search_url = f"{self.base_url}/catalog/search"
        params = {
            "query": product_name,
            "_search": product_name,
            "page": 1,
            "resultsPerPage": 10,
            "dataType": "product",
            "sort": "most-active"
        }
        
        data = self._make_request(search_url, params)
        
        if not data.get('hits'):
            raise ValueError(f"No results found for '{product_name}'")
            
        # Get the first matching product
        product = data['hits'][0]
        
        # Get detailed product info
        product_url = f"{self.base_url}/catalog/variants/{product.get('objectID')}"
        product_data = self._make_request(product_url)
        
        if not product_data:
            raise ValueError("Could not fetch product details")
            
        return product_data

    def get_price_data(self, product_name: str, size: float) -> Tuple[float, float, float]:
        """
        Get pricing data for a specific shoe and size.
        
        Args:
            product_name: Name of the shoe
            size: Shoe size
            
        Returns:
            Tuple of (bid, ask, payout) prices
        """
        try:
            product = self.get_product_info(product_name)
            
            # Find the matching size variant
            size_str = str(size)
            variants = product.get('variants', [])
            variant = next(
                (v for v in variants if v.get('size') == size_str),
                None
            )
            
            if not variant:
                raise ValueError(f"Size {size} not found for {product_name}")
                
            # Extract market data
            market = variant.get('market', {})
            bid = float(market.get('highestBid', 0))
            ask = float(market.get('lowestAsk', 0))
            payout = bid * 0.9  # StockX takes ~10% fee
            
            return bid, ask, payout
            
        except Exception as e:
            raise ValueError(f"Error getting price data: {str(e)}")
