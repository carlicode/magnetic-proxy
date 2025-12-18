#!/usr/bin/env python3
"""
Ejemplo de scraping de productos usando magnetic proxy.

Este script demuestra cómo usar los módulos del proyecto para hacer scraping
de productos de manera ética y legal a través del proxy magnetic.

Uso:
    python examples/product_scraper.py
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config.settings import ProxyConfig, ScraperConfig
from src.proxy.client import ProxyClient
from src.scraper.parser import parse_products_page, get_next_page_url


def main():
    """
    Función principal que orquesta el scraping de productos.
    """
    print("=" * 60)
    print("Ejemplo de Scraping de Productos con Magnetic Proxy")
    print("=" * 60)
    print()
    
    # Configuración del proxy
    # Opción 1: Desde variables de entorno (recomendado para producción)
    try:
        proxy_config = ProxyConfig.from_env()
        print("✓ Configuración del proxy cargada desde variables de entorno")
    except ValueError:
        # Opción 2: Configuración manual (solo para ejemplos/testing)
        print("⚠ Variables de entorno no encontradas, usando configuración manual")
        print("  Para usar variables de entorno, configura:")
        print("    export MAGNETIC_PROXY_USER='tu-usuario'")
        print("    export MAGNETIC_PROXY_PASSWORD='tu-password'")
        print()
        
        # Opción 2: Configuración manual (solo para ejemplos/testing)
        # Reemplaza con tus credenciales reales o crea un archivo .env
        proxy_config = ProxyConfig(
            user="customer-carli.f.roman-cc-us-hardcountry-true-sessid-proxy-sample-sesstime-1",
            password="<proxy_user_password>"  # ⚠️ Reemplaza con tu password real
        )
    
    # Configuración del scraper
    scraper_config = ScraperConfig(
        base_url="https://books.toscrape.com",
        timeout=10,
        delay_between_requests=1.0
    )
    
    # Crear cliente del proxy
    client = ProxyClient(proxy_config, delay=scraper_config.delay_between_requests)
    
    print(f"✓ Cliente del proxy inicializado")
    print(f"✓ URL base: {scraper_config.base_url}")
    print()
    
    # Iniciar scraping
    all_products = []
    current_url = scraper_config.base_url
    max_pages = 2  # Limitar a 2 páginas para el ejemplo
    
    try:
        page_count = 0
        while current_url and page_count < max_pages:
            page_count += 1
            print(f"📄 Obteniendo página {page_count}: {current_url}")
            
            # Hacer request a través del proxy
            response = client.get(current_url)
            print(f"✓ Respuesta recibida (status: {response.status_code})")
            
            # Parsear productos de la página
            products = parse_products_page(response.text, scraper_config.base_url)
            print(f"✓ {len(products)} productos encontrados en esta página")
            
            all_products.extend(products)
            
            # Mostrar algunos productos de ejemplo
            if products:
                print("\n  Ejemplos de productos encontrados:")
                for i, product in enumerate(products[:3], 1):
                    print(f"    {i}. {product['title']}")
                    print(f"       Precio: {product['price']}")
                    print(f"       Disponibilidad: {product['availability']}")
                    print(f"       Rating: {product['rating']}")
                    print()
            
            # Buscar siguiente página
            next_url = get_next_page_url(response.text, scraper_config.base_url)
            if next_url:
                current_url = next_url
                print(f"→ Siguiente página encontrada: {next_url}")
            else:
                print("→ No hay más páginas")
                break
            
            print("-" * 60)
            print()
        
        # Resumen final
        print("=" * 60)
        print("RESUMEN")
        print("=" * 60)
        print(f"Total de productos encontrados: {len(all_products)}")
        print(f"Páginas procesadas: {page_count}")
        print()
        
        # Mostrar algunos productos destacados
        if all_products:
            print("Algunos productos encontrados:")
            for i, product in enumerate(all_products[:5], 1):
                print(f"\n{i}. {product['title']}")
                print(f"   Precio: {product['price']}")
                print(f"   Disponibilidad: {product['availability']}")
                print(f"   Rating: {product['rating']}")
                if product['link']:
                    print(f"   Link: {product['link']}")
        
    except Exception as e:
        print(f"\n❌ Error durante el scraping: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

