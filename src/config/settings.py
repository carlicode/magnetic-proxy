"""
Configuración centralizada del proyecto.
Maneja credenciales del proxy, URLs y constantes.
"""

import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

# Cargar variables de entorno desde .env si existe
try:
    from dotenv import load_dotenv
    # Buscar .env en el directorio raíz del proyecto
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # Si python-dotenv no está instalado, continuar sin él
    pass


@dataclass
class ProxyConfig:
    """Configuración del proxy magnetic."""
    user: str
    password: str
    host: str = "rs.magneticproxy.net"
    port: str = "443"
    
    @classmethod
    def from_env(cls) -> 'ProxyConfig':
        """
        Crea configuración desde variables de entorno.
        
        Variables esperadas:
        - MAGNETIC_PROXY_USER: Usuario del proxy
        - MAGNETIC_PROXY_PASSWORD: Contraseña del proxy
        - MAGNETIC_PROXY_HOST: Host del proxy (opcional, default: rs.magneticproxy.net)
        - MAGNETIC_PROXY_PORT: Puerto del proxy (opcional, default: 443)
        """
        user = os.getenv('MAGNETIC_PROXY_USER')
        password = os.getenv('MAGNETIC_PROXY_PASSWORD')
        host = os.getenv('MAGNETIC_PROXY_HOST', 'rs.magneticproxy.net')
        port = os.getenv('MAGNETIC_PROXY_PORT', '443')
        
        if not user or not password:
            raise ValueError(
                "MAGNETIC_PROXY_USER y MAGNETIC_PROXY_PASSWORD deben estar configurados "
                "como variables de entorno o pasados directamente."
            )
        
        return cls(user=user, password=password, host=host, port=port)
    
    def get_proxy_url(self) -> str:
        """Retorna la URL completa del proxy con autenticación."""
        return f"https://{self.user}:{self.password}@{self.host}:{self.port}"


@dataclass
class ScraperConfig:
    """Configuración para el scraper."""
    base_url: str = "https://books.toscrape.com"
    timeout: int = 10
    delay_between_requests: float = 1.0  # Segundos entre requests
    max_retries: int = 3

