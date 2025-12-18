"""
Funciones para parsear HTML y extraer datos de productos.
"""

from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup


def parse_product(soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
    """
    Extrae información de un producto desde un elemento BeautifulSoup.
    
    Args:
        soup: BeautifulSoup object del HTML de un producto
        
    Returns:
        Diccionario con la información del producto o None si no se puede parsear
    """
    try:
        # Extraer título
        title_elem = soup.select_one('h3 a')
        title = title_elem.get('title', '').strip() if title_elem else ''
        
        # Extraer precio
        price_elem = soup.select_one('.price_color')
        price = price_elem.text.strip() if price_elem else 'N/A'
        
        # Extraer disponibilidad
        availability_elem = soup.select_one('.availability')
        availability = availability_elem.text.strip() if availability_elem else 'N/A'
        
        # Extraer rating (estrellas)
        rating_elem = soup.select_one('.star-rating')
        rating = rating_elem.get('class', [])[-1] if rating_elem else 'N/A'
        
        # Extraer link del producto
        link_elem = soup.select_one('h3 a')
        link = link_elem.get('href', '') if link_elem else ''
        
        return {
            'title': title,
            'price': price,
            'availability': availability,
            'rating': rating,
            'link': link
        }
    except Exception as e:
        print(f"Error al parsear producto: {str(e)}")
        return None


def parse_products_page(html: str, base_url: str = "https://books.toscrape.com") -> List[Dict[str, Any]]:
    """
    Parsea una página de productos y extrae todos los productos.
    
    Args:
        html: HTML de la página de productos
        base_url: URL base para construir links completos
        
    Returns:
        Lista de diccionarios con información de cada producto
    """
    soup = BeautifulSoup(html, 'lxml')
    products = []
    
    # Buscar todos los elementos de productos (en books.toscrape.com están en article.product_pod)
    product_elements = soup.select('article.product_pod')
    
    for product_elem in product_elements:
        product_data = parse_product(product_elem)
        if product_data:
            # Convertir link relativo a absoluto si es necesario
            if product_data['link'] and not product_data['link'].startswith('http'):
                product_data['link'] = base_url + '/' + product_data['link'].lstrip('/')
            products.append(product_data)
    
    return products


def get_next_page_url(html: str, base_url: str = "https://books.toscrape.com") -> Optional[str]:
    """
    Extrae la URL de la siguiente página si existe.
    
    Args:
        html: HTML de la página actual
        base_url: URL base para construir links completos
        
    Returns:
        URL de la siguiente página o None si no hay más páginas
    """
    soup = BeautifulSoup(html, 'lxml')
    next_link = soup.select_one('li.next a')
    
    if next_link:
        href = next_link.get('href', '')
        if href:
            if not href.startswith('http'):
                href = base_url + '/' + href.lstrip('/')
            return href
    
    return None

