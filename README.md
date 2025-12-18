# Magnetic Proxy - Ejemplo de Scraping Modular

Este proyecto demuestra cómo usar **Magnetic Proxy** para hacer scraping de productos de manera ética y legal, utilizando una arquitectura modular y reutilizable.

## 📁 Estructura del Proyecto

```
magnetic-proxy/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Configuración centralizada
│   ├── proxy/
│   │   ├── __init__.py
│   │   └── client.py             # Cliente reutilizable para el proxy
│   └── scraper/
│       ├── __init__.py
│       └── parser.py             # Funciones de parsing HTML
├── examples/
│   └── product_scraper.py        # Ejemplo completo de uso
├── requirements.txt
└── README.md
```

## 🏗️ Arquitectura Modular

### `src/config/settings.py`
Módulo de configuración centralizada que maneja:
- Credenciales del proxy (pueden venir de variables de entorno)
- URLs base para scraping
- Timeouts y delays configurables
- Constantes reutilizables

### `src/proxy/client.py`
Cliente del proxy que encapsula toda la lógica de conexión:
- Clase `ProxyClient` con métodos `get()` y `post()`
- Manejo automático de delays entre requests
- Manejo de errores de conexión
- Reutilizable para cualquier tipo de request HTTP

### `src/scraper/parser.py`
Funciones para parsear HTML y extraer datos:
- `parse_product()`: Extrae información de un producto individual
- `parse_products_page()`: Parsea una página completa de productos
- `get_next_page_url()`: Encuentra la URL de la siguiente página
- Fácil de adaptar para otros sitios web

### `examples/product_scraper.py`
Script de ejemplo que demuestra:
- Cómo configurar el proxy
- Cómo usar el `ProxyClient` para hacer requests
- Cómo parsear y extraer datos de productos
- Manejo de paginación
- Output de resultados

## 🚀 Instalación

### 1. Crear un entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### Opción 1: Archivo .env (Más Fácil y Recomendado) ⭐

1. Crea un archivo `.env` en la raíz del proyecto:

```bash
# Crear el archivo .env
touch .env
```

2. Agrega tus credenciales al archivo `.env`:

```env
MAGNETIC_PROXY_USER=carli.f.roman
MAGNETIC_PROXY_PASSWORD=tu_password_real_aqui
MAGNETIC_PROXY_HOST=rs.magneticproxy.net
MAGNETIC_PROXY_PORT=443
```

**Nota**: El formato del usuario puede variar. Usa exactamente el que te muestre el panel de Magnetic Proxy (puede ser solo `carli.f.roman` o el formato completo `customer-...`).

**⚠️ Importante**: Reemplaza `tu_password_real_aqui` con tu contraseña real del proxy.

3. El proyecto cargará automáticamente las variables desde el archivo `.env` cuando ejecutes el script.

### Opción 2: Variables de Entorno del Sistema

Configura las credenciales del proxy como variables de entorno:

```bash
export MAGNETIC_PROXY_USER="carli.f.roman"
export MAGNETIC_PROXY_PASSWORD="tu_password_real"
export MAGNETIC_PROXY_HOST="rs.magneticproxy.net"  # Opcional
export MAGNETIC_PROXY_PORT="443"                   # Opcional
```

### Opción 3: Configuración Manual en el Código

Puedes editar directamente `examples/product_scraper.py` y modificar las credenciales en la función `main()` (líneas 48-51).

## 📖 Uso

### Ejecutar el ejemplo básico

**Pasos rápidos:**

```bash
# 1. Activar el entorno virtual
source venv/bin/activate

# 2. Ejecutar el script
python3 examples/product_scraper.py
```

**O en una sola línea:**

```bash
source venv/bin/activate && python3 examples/product_scraper.py
```

**Qué hace el script:**
1. ✅ Se conecta al proxy usando tus credenciales del archivo `.env`
2. ✅ Hace scraping de productos desde `books.toscrape.com` (sitio diseñado para práctica)
3. ✅ Extrae: título, precio, disponibilidad, rating
4. ✅ Muestra los resultados en consola
5. ✅ Maneja paginación automáticamente

### Usar los módulos en tu propio código

```python
from src.config.settings import ProxyConfig, ScraperConfig
from src.proxy.client import ProxyClient
from src.scraper.parser import parse_products_page

# Configurar proxy
proxy_config = ProxyConfig.from_env()  # O crear manualmente
client = ProxyClient(proxy_config, delay=1.0)

# Hacer request a través del proxy
response = client.get("https://books.toscrape.com")

# Parsear productos
products = parse_products_page(response.text)

# Usar los datos
for product in products:
    print(f"{product['title']}: {product['price']}")
```

## 🔧 Personalización

### Cambiar el sitio a scrapear

1. Modifica `ScraperConfig.base_url` en `examples/product_scraper.py`
2. Ajusta las funciones de parsing en `src/scraper/parser.py` según la estructura HTML del nuevo sitio

### Ajustar delays y timeouts

Modifica `ScraperConfig` en tu código:

```python
scraper_config = ScraperConfig(
    timeout=15,                    # Timeout más largo
    delay_between_requests=2.0     # Más tiempo entre requests
)
```

### Usar el ProxyClient para otros tipos de requests

El `ProxyClient` no está limitado a scraping. Puedes usarlo para cualquier request HTTP:

```python
# GET request
response = client.get("https://api.example.com/data")

# POST request
response = client.post(
    "https://api.example.com/submit",
    json={"key": "value"}
)
```

## ⚠️ Consideraciones Éticas

Este ejemplo está diseñado para ser ético y legal:

- ✅ Usa `books.toscrape.com`, un sitio diseñado específicamente para práctica de scraping
- ✅ Incluye delays entre requests para no sobrecargar el servidor
- ✅ Respeta los límites del sitio
- ✅ Solo extrae información pública

**Importante**: Al usar este código con otros sitios, asegúrate de:
- Revisar y respetar `robots.txt`
- Verificar los términos de servicio del sitio
- Usar delays apropiados entre requests
- No hacer requests excesivos que puedan sobrecargar el servidor

## 🐛 Solución de Problemas

### Error: "MAGNETIC_PROXY_USER y MAGNETIC_PROXY_PASSWORD deben estar configurados"

**Solución**: Configura las variables de entorno o edita las credenciales directamente en el código.

### Error: "Connection timeout"

**Solución**: 
- Verifica que las credenciales del proxy sean correctas
- Aumenta el timeout en `ScraperConfig`
- Verifica tu conexión a internet

### Error: "ModuleNotFoundError"

**Solución**: Asegúrate de haber instalado las dependencias:
```bash
pip install -r requirements.txt
```

## 📝 Dependencias

- `requests`: Para hacer HTTP requests a través del proxy
- `beautifulsoup4`: Para parsear HTML
- `lxml`: Parser rápido para BeautifulSoup
- `python-dotenv`: Para cargar variables de entorno desde archivo `.env`

## 🎬 Demo en Video

¿Quieres ver cómo funciona? Revisa el video tutorial en TikTok donde explico paso a paso cómo usar este proyecto.

## 🤝 Contribuir

Este es un proyecto de ejemplo. Siéntete libre de:
- Adaptar el código para tus necesidades
- Agregar nuevos parsers para otros sitios
- Mejorar el manejo de errores
- Agregar funcionalidades adicionales

## 📄 Licencia

Este proyecto es un ejemplo educativo. Úsalo responsablemente y respeta los términos de servicio de los sitios que visites.
