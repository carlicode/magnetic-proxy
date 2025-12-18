"""
Módulo de scraping.
Contiene funciones para parsear HTML y extraer datos.
"""

from .parser import parse_product, parse_products_page

__all__ = ['parse_product', 'parse_products_page']

