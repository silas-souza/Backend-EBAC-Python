import requests
import time
import csv
import random
import json
import concurrent.futures
import re
from bs4 import BeautifulSoup

# Headers mais completos para parecer um humano navegando
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.google.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
}

MAX_THREADS = 2 # Manter baixo para evitar banimento de IP

def extract_movie_details(movie_link):
    time.sleep(random.uniform(2, 5)) 
    try:
        # Criando uma sessão para manter cookies básicos
        session = requests.Session()
        response = session.get(movie_link, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"⚠️ Acesso negado ao filme (Status {response.status_code})")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        json_script = soup.find('script', type='application/ld+json')
        
        if json_script:
            data = json.loads(json_script.string)
            title = data.get('name', 'N/A')
            rating = data.get('aggregateRating', {}).get('ratingValue', 'N/A')
            plot_text = data.get('description', 'N/A')
            date = data.get('datePublished', 'N/A')[:4]
        else:
            # Fallback manual caso o JSON não esteja presente
            title = soup.find('h1').get_text().strip() if soup.find('h1') else "N/A"
            rating = "N/A"
            plot_text = "N/A"
            date = "N/A"

        with open('movies.csv', mode='a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([title, date, rating, plot_text])
            print(f"✅ Extraído com sucesso: {title}")

    except Exception as e:
        print(f"❌ Erro ao processar detalhes: {e}")

def extract_movies(url):
    print(f"Tentando acessar: {url}")
    session = requests.Session()
    response = session.get(url, headers=headers, timeout=20)
    
    if response.status_code != 200:
        print(f"Falha na página inicial. Status: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Busca por links de filmes usando Expressão Regular (mais estável)
    # Procuramos por padrões como /title/tt1234567/
    links = soup.find_all('a', href=re.compile(r'\/title\/tt\d+'))
    
    movie_links = []
    for link in links:
        path = link['href'].split('?')[0]
        full_url = "https://www.imdb.com" + path
        if full_url not in movie_links:
            movie_links.append(full_url)

    # Pegamos os primeiros 20 para testar se está funcionando
    movie_links = movie_links[:20]
    
    if not movie_links:
        print("🛑 Nenhum filme encontrado. O IMDb bloqueou a leitura da lista.")
        return

    print(f"Encontrados {len(movie_links)} filmes. Iniciando extração...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(extract_movie_details, movie_links)

def main():
    # Inicializa o CSV
    with open('movies.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Titulo', 'Data', 'Nota', 'Resumo'])

    start_url = 'https://www.imdb.com/chart/moviemeter/'
    extract_movies(start_url)
    print("\nProcesso finalizado. Verifique o arquivo movies.csv")

if __name__ == '__main__':
    main()