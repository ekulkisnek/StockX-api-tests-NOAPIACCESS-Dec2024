"""
StockX API client module using Algolia search to fetch StockX product data.
"""
from algoliasearch.search_client import SearchClient
from typing import Dict, Tuple

class StockXAPI:
    def __init__(self):
        """Initialize the Algolia client with StockX's credentials."""
        self.client = SearchClient.create(
            'XW7SBCT9V6',  # Application ID
            '6b5e76b49705eb9f51a06d3c82f7acee'  # API Key
        )
        self.index = self.client.init_index('products')

    def get_product_info(self, product_name: str) -> Dict:
        """
        Search for a product using Algolia search.
        
        Args:
            product_name: Name of the shoe to search for
            
        Returns:
            Dict containing product information including variants
        """
        # Search for the product
        results = self.index.search(product_name, {
            'hitsPerPage': 1,  # We only need the first result
            'filters': 'type:sneakers'  # Only search for sneakers
        })

        if not results['hits']:
            raise ValueError(f"No results found for '{product_name}'")

        return results['hits'][0]

    def get_price_data(self, product_name: str, size: float) -> Tuple[float, float, float]:
        """
        Get pricing data for a specific shoe and size.
        
        Args:
            product_name: Name of the shoe
            size: Shoe size
            
        Returns:
            Tuple of (bid, ask, payout) prices
        """
        product_info = self.get_product_info(product_name)
        
        # Look for the size variant in the product data
        variants = product_info.get('variants', [])
        size_str = str(size)
        
        for variant in variants:
            if variant.get('size') == size_str:
                market_data = variant.get('market', {})
                bid = float(market_data.get('highestBid', 0))
                ask = float(market_data.get('lowestAsk', 0))
                # Payout is typically 90% of the bid price
                payout = bid * 0.9
                return bid, ask, payout
                
        raise ValueError(f"Size {size} not found for {product_name}")
