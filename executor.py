import os
import time
import re
import libtorrent as lt
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import schedule
from datetime import datetime

# Configuração do diretório para salvar torrents
torrents_directory = './torrents'

# Verifica se o diretório de torrents existe, caso contrário, cria-o
if not os.path.exists(torrents_directory):
    os.makedirs(torrents_directory)

def get_new_movies():
    options = Options()
    options.headless = False  # True para rodar sem abrir a janela do navegador

    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.get('https://comando.la/')

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.post')))

        movie_elements = driver.find_elements(By.CSS_SELECTOR, '.post')
        movies = []

        for movie_element in movie_elements:
            title_element = movie_element.find_element(By.CSS_SELECTOR, 'h2 a')
            title = title_element.text
            link = title_element.get_attribute('href')
            movies.append({'title': title, 'link': link})

        print('Novos filmes encontrados:', movies)

        for movie in movies:
            process_movie(driver, movie)

    except Exception as e:
        print(f'Erro ao buscar novos filmes: {e}')
    finally:
        driver.quit()

def process_movie(driver, movie):
    try:
        print(f'Processando filme: {movie["title"]}')
        driver.get(movie['link'])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.customButton')))

        is_quality_acceptable = driver.execute_script("""
            const paragraphs = document.querySelectorAll('p[style="text-align: center;"]');
            let hasDualAudio = false;
            let hasWebDl1080p = false;

            paragraphs.forEach(p => {
                if (p.innerText.includes('DUAL ÁUDIO')) {
                    hasDualAudio = true;
                }
                if (p.innerText.includes('WEB-DL 1080p Dual Áudio 5.1')) {
                    hasWebDl1080p = true;
                }
            });

            return hasDualAudio && hasWebDl1080p;
        """)

        # Adicionando a condição de que o título deve conter "WEB-DL"
        if not is_quality_acceptable and "WEB-DL" not in movie["title"]:
            print(f'Filme: {movie["title"]} não possui a qualidade necessária WEB-DL 1080p Dual Áudio 5.1 ou título não contém "WEB-DL".')
            return

        download_link = get_download_link(driver)

        if download_link:
            movie['downloadLink'] = download_link
            print(f'Filme: {movie["title"]}')
            print(f'Link de Download: {movie["downloadLink"]}')
            convert_magnet_to_torrent(download_link, sanitize_title(movie['title']))
        else:
            print(f'Link de download não encontrado para o filme: {movie["title"]}')
    except Exception as e:
        print(f'Erro ao processar filme {movie["title"]}: {e}')

def get_download_link(driver):
    try:
        return driver.execute_script("""
            const paragraphs = document.querySelectorAll('p[style="text-align: center;"]');
            let downloadLink = null;

            paragraphs.forEach(p => {
                const strongElements = p.querySelectorAll('strong');
                if (strongElements.length > 0 && strongElements[0].innerText.includes('DUAL ÁUDIO')) {
                    const nextP = p.nextElementSibling;
                    if (nextP && nextP.innerText.includes('WEB-DL 1080p Dual Áudio 5.1')) {
                        const aTag = nextP.querySelector('a.customButton');
                        if (aTag && aTag.href.includes('magnet') && !aTag.href.includes('HDCAM')) {
                            downloadLink = aTag.href;
                        }
                    }
                }
            });

            return downloadLink;
        """)
    except Exception as e:
        print(f'Erro ao obter o link de download: {e}')
        return None

def sanitize_title(title):
    return re.sub(r'[^a-zA-Z0-9]', '_', title).strip()

def convert_magnet_to_torrent(magnet_uri, title):
    ses = lt.session()
    params = {
        'save_path': torrents_directory,
        'storage_mode': lt.storage_mode_t.storage_mode_sparse
    }
    handle = lt.add_magnet_uri(ses, magnet_uri, params)
    print(f'Iniciando download do magnet link: {magnet_uri}')

    while not handle.has_metadata():
        time.sleep(1)

    torrent_file_path = os.path.join(torrents_directory, f'{title}.torrent')  # Corrigindo a extensão do arquivo
    torrent_info = handle.get_torrent_info()
    torrent = lt.create_torrent(torrent_info)
    torrent.set_creator("Libtorrent")
    torrent.set_comment("Generated by Libtorrent")
    
    with open(torrent_file_path, 'wb') as f:
        f.write(lt.bencode(torrent.generate()))
    
    print(f'Arquivo .torrent salvo em: {torrent_file_path}')

def schedule_task(hour, minute):
    schedule_time = f"{hour:02d}:{minute:02d}"
    try:
        schedule.every().day.at(schedule_time).do(get_new_movies)
        print(f"Aplicação agendada para {schedule_time} todos os dias.")
    except schedule.ScheduleValueError as e:
        print(f"Erro ao agendar: {e}")

def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    # Defina a hora e o minuto desejados aqui
    hour = 11
    minute = 44

    # Agende a tarefa
    schedule_task(hour, minute)
    
    print("Pressione Ctrl+C para sair.")
    
    # Inicia o agendador em um loop infinito
    start_scheduler()

if __name__ == "__main__":
    main()
