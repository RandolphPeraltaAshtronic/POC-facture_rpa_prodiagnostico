import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def initialize_chrome_driver(headless: bool = False, download_dir: str = None) -> webdriver.Chrome:
    """
    Establece y configura una conexión con el navegador Chrome utilizando Selenium WebDriver.
    Adaptado para funcionar en Docker utilizando una variable de entorno RUNNING_IN_DOCKER.

    Args:
        headless (bool): Si se desea iniciar el navegador sin interfaz gráfica.
                         En Docker, se fuerza a True a menos que se anule explícitamente.
        download_dir (str): Directorio para descargas.

    Returns:
        WebDriver: Instancia de Selenium WebDriver configurada para Chrome.
    """
    chrome_options = webdriver.ChromeOptions()
    
    #running_in_docker = os.environ.get("RUNNING_IN_DOCKER", "false").lower() == "true"

    '''if running_in_docker:
        effective_headless = True  # Forzar headless si se ejecuta en Docker
    else:'''
    effective_headless = headless

    if effective_headless:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox") # Añadido para mayor compatibilidad en Docker
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu") # Necesario para headless en algunos entornos
    chrome_options.add_argument("--window-size=1920x1080") # Puede ayudar con algunos sitios web

    if download_dir:
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
        }
        chrome_options.add_experimental_option("prefs", prefs)

    '''if running_in_docker:
        # En Docker, se asume que chromedriver está en el PATH (/usr/local/bin/chromedriver)
        # o se puede especificar la ruta directamente.
        # Service() sin argumentos debería encontrarlo si está en el PATH.
        # Para mayor certeza, se puede especificar:
        service = Service(executable_path='/usr/local/bin/chromedriver')
    else:'''
    # Selenium 4.6.0+ includes its own driver manager.
    # Initializing Service() without arguments will automatically
    # download and manage the required chromedriver.
    service = Service()
        
    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
    
    # Maximizar ventana puede no tener mucho efecto en headless, pero se mantiene por consistencia
    if not effective_headless:
        driver.maximize_window()
        
    return driver