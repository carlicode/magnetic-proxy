"""
Cliente para hacer requests HTTP a través del proxy magnetic.
"""

import time
import requests
from typing import Optional, Dict, Any
from ..config.settings import ProxyConfig


class ProxyClient:
    """
    Cliente que encapsula la lógica de hacer requests a través del proxy.
    
    Ejemplo de uso:
        config = ProxyConfig(user="...", password="...")
        client = ProxyClient(config)
        response = client.get("https://example.com")
    """
    
    def __init__(self, config: ProxyConfig, delay: float = 1.0):
        """
        Inicializa el cliente del proxy.
        
        Args:
            config: Configuración del proxy
            delay: Tiempo en segundos a esperar entre requests (para ser respetuoso)
        """
        self.config = config
        self.delay = delay
        self.proxy_url = config.get_proxy_url()
        self.proxies = {
            "http": self.proxy_url,
            "https": self.proxy_url
        }
        self.last_request_time = 0
    
    def _wait_if_needed(self):
        """Espera el delay configurado si es necesario."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.delay:
            time.sleep(self.delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """
        Hace un GET request a través del proxy.
        
        Args:
            url: URL a la que hacer el request
            **kwargs: Argumentos adicionales para requests.get()
            
        Returns:
            Response object de requests
            
        Raises:
            requests.RequestException: Si el request falla
        """
        self._wait_if_needed()
        
        # Asegurar que use los proxies configurados
        kwargs.setdefault('proxies', self.proxies)
        kwargs.setdefault('timeout', 10)
        
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise requests.RequestException(
                f"Error al hacer GET request a {url} a través del proxy: {str(e)}"
            ) from e
    
    def post(self, url: str, data: Optional[Dict[str, Any]] = None, 
             json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Hace un POST request a través del proxy.
        
        Args:
            url: URL a la que hacer el request
            data: Datos a enviar (form-encoded)
            json: Datos JSON a enviar
            **kwargs: Argumentos adicionales para requests.post()
            
        Returns:
            Response object de requests
            
        Raises:
            requests.RequestException: Si el request falla
        """
        self._wait_if_needed()
        
        # Asegurar que use los proxies configurados
        kwargs.setdefault('proxies', self.proxies)
        kwargs.setdefault('timeout', 10)
        
        try:
            response = requests.post(url, data=data, json=json, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise requests.RequestException(
                f"Error al hacer POST request a {url} a través del proxy: {str(e)}"
            ) from e

