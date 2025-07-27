# IMDb Scraper


Este proyecto utiliza Scrapy para extraer información de IMDb. Se eligió Scrapy porque es una herramienta robusta, eficiente y altamente mantenible, ideal para proyectos de scraping de tamaño mediano a grande. Scrapy permite estructurar el código de forma modular, facilita la gestión de grandes volúmenes de datos y cumple con los requerimientos de robustez y eficiencia solicitados.

**Acceso y extracción de datos:**
- Se utilizan headers personalizados para simular un navegador real y evitar bloqueos, pero no es necesario manejar cookies, ya que las páginas de referencia (por ejemplo, https://www.imdb.com/chart/top/) permiten el acceso sin iniciar sesión.
- El scraping se realiza mediante simples peticiones GET, ya que toda la información relevante se encuentra incrustada en el tag `<script id="__NEXT_DATA__" type="application/json">` dentro del HTML.
- El proceso consiste en extraer ese bloque JSON y parsearlo para obtener los códigos de las películas y actores.
- Posteriormente, se realiza un GET a la página de detalle de cada película (por ejemplo, https://www.imdb.com/es-es/title/tt0111161/) usando el código obtenido en el primer JSON, para extraer información adicional y detallada de cada título.

Además, se utiliza una conexión de Supabase para facilitar el testing con PostgreSQL. Sin embargo, toda la lógica de conexión a base de datos está abstraída mediante el patrón Adapter, lo que permite cambiar fácilmente a MySQL u otra base de datos relacional implementando únicamente un nuevo manager. Por ejemplo, la implementación actual para PostgreSQL se encuentra en:

`data/table_manager.py` (clase `PostgresManager`)

Para migrar a otra base de datos, solo es necesario crear un manager equivalente y ajustar la configuración, sin modificar el resto del proyecto.

## Nota sobre ejecución de spiders

También se implementó el patrón Factory en `run_spider.py` para permitir la ejecución de cualquier spider simplemente cambiando el nombre. Sin embargo, esto no es estrictamente necesario, ya que la propia interfaz de línea de comandos de Scrapy ya permite ejecutar cualquier spider de forma sencilla, como se muestra en la sección "Cómo iniciar el proyecto".

## Entregables

A continuación se incluyen los principales entregables del proyecto, disponibles en la carpeta `files`:


- [Repocitorio Git](https://github.com/wzuniga/test-scraping-imdb)
- [Script SQL: creación de tablas, vistas e índices](files/database.sql)
- [Archivo CSV generado para actores](files/database_actors.csv)
- [Archivo CSV generado para películas](files/database_movies.csv)

### Logs de ejecución

En la carpeta principal del proyecto se generan archivos de log con el detalle de la ejecución de los spiders, por ejemplo:

- [`movies_output.log`](movies_output.log): Log de ejecución del spider de películas.
- [`actors_output.log`](actors_output.log): Log de ejecución del spider de actores.

En ambos casos se utilizan proxies rotativos: se configuran 3 proxies y un sistema de reintentos de hasta 3 veces, todo parametrizable desde el archivo `.env`. Esta lógica de rotación y backoff de proxies se gestiona automáticamente gracias a la configuración en `settings.py`, aprovechando las capacidades nativas de Scrapy para manejar reintentos y backoff de manera eficiente (otro motivo clave para elegir Scrapy en este proyecto). Los proxies usados se muestran en el log solo cuando el resultado fue exitoso; en caso de falla, Scrapy lo maneja internamente y usa la configuración de backoff definida en `settings.py`.

**Nota sobre proxies y logs:**
En los logs de ejecución, se puede observar mensajes como:

```
2025-07-27 00:40:49 [rotating_proxies.middlewares] INFO: Proxies(good: 0, dead: 0, unchecked: 3, reanimated: 0, mean backoff time: 0s)
```
Esto indica la cantidad de proxies configurados y su estado (buenos, caídos, sin verificar, reanimados, etc.). En este caso, no se logró conseguir un proxy público que funcionara correctamente, por lo que se utilizó un proxy local creado con:

```
mitmproxy --mode regular --listen-port 8080
```
Puedes usar mitmproxy o cualquier otro proxy local para pruebas si no cuentas con proxies públicos funcionales. El sistema de rotación y backoff seguirá funcionando y registrando el estado de los proxies en los logs.

**Sobre la lista de proxies:**
En la configuración (`settings.py`), la variable `ROTATING_PROXY_LIST` incluye tanto proxies públicos como un proxy local, por ejemplo:

```
ROTATING_PROXY_LIST = [
    'http://51.158.68.68:8811',
    'http://185.199.228.140:7300',
    'http://127.0.0.1:8080'
]
```
Esto permite que, si los proxies públicos fallan o no están disponibles, Scrapy termine utilizando el proxy local (`127.0.0.1:8080`) para realizar la conexión. Así, el scraping no se detiene.

## Requisitos
- Python 3.8+
- pip

## Instalación del entorno

1. **Crea un entorno virtual:**
   ```sh
   python -m venv venv
   ```

2. **Activa el entorno virtual:**
   - En Windows:
     ```sh
     venv\Scripts\activate
     ```
   - En Mac/Linux:
     ```sh
     source venv/bin/activate
     ```

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```
   Esto instalará todas las dependencias necesarias, incluyendo `psycopg2-binary` para la conexión a PostgreSQL.

4. **Configura las variables de entorno:**
   - Se está agregando un `.env` válido para pruebas.
   - Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
     ```env
     IMDB_TOP_URL=https://www.imdb.com/chart/top/
     POSTGRESQL_URL=postgresql://postgres.wzriqyckzwkdxuudycoq:[TU-PASSWORD]@aws-0-us-east-2.pooler.supabase.com:6543/postgres
     LOG_FILE=response.log
     LOG_LEVEL=INFO
     USE_PROXY=true
     RETRY_TIMES=5
     ```
   - Ajusta los valores según tu entorno y base de datos.

## Cómo iniciar el proyecto

1. Asegúrate de que el entorno virtual esté activado.
2. Ejecuta uno de los siguientes spiders según la información que quieras extraer:
   - **Películas:**
     ```sh
     scrapy crawl imdb_movie
     ```
   - **Actores:**
     ```sh
     scrapy crawl imdb_actor
     ```
   - **Películas y actores combinados:**
     ```sh
     scrapy crawl imdb_movies_actors
     ```

Esto iniciará el scraping usando la URL definida en el archivo `.env` con el spider seleccionado.

---
