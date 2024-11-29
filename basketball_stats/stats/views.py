import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

# URL do Proxy (CORS Anywhere)
PROXY_URL = 'http://localhost:8080/'
URLS = [
    'https://betsapi.com/r/8671360/DEN-Nuggets-vs-LA-Lakers',
    'https://betsapi.com/r/8671055/DAL-Mavericks-vs-DEN-Nuggets'
]

def fetch_data(url):
    """Função para buscar os dados da URL fornecida com proxy."""
    proxied_url = PROXY_URL + url  # Concatenando a URL do CORS Anywhere com o destino

    try:
        # Usando o proxy para fazer a requisição com timeout para evitar travamentos
        response = requests.get(proxied_url, timeout=10)
        response.raise_for_status()  # Levanta uma exceção para erros HTTP (status > 400)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extrair os dados de tabelas conforme o modelo
        data_rows = []
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            data = [col.text.strip() for col in cols]
            if data:
                data_rows.append(data)

        return data_rows

    except requests.exceptions.ProxyError as e:
        # Log para erro de Proxy
        print(f"Erro de Proxy ao acessar {url}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        # Log para outros erros de requisição
        print(f"Erro ao fazer requisição para {url}: {e}")
        return None

def index(request):
    """Função para renderizar os dados no template."""
    all_data = []
    # Iterando pelas URLs e buscando os dados
    for url in URLS:
        data = fetch_data(url)
        if data:
            all_data.append(data)
    
    # Verificando se conseguimos coletar dados de pelo menos um jogo
    if not all_data:
        return render(request, 'stats/index.html', {'error': 'Não foi possível recuperar dados de nenhum jogo.'})

    # Calcular médias (exemplo: média dos pontos)
    total_stats = {}
    games = len(all_data)

    for game_data in all_data:
        for row in game_data:
            stat_name = row[1]
            team1_val = int(row[0]) if row[0].isdigit() else 0
            team2_val = int(row[2]) if row[2].isdigit() else 0

            if stat_name not in total_stats:
                total_stats[stat_name] = [0, 0]  # [Team1 total, Team2 total]
            total_stats[stat_name][0] += team1_val
            total_stats[stat_name][1] += team2_val

    # Calcular a média de cada estatística
    avg_stats = {stat: [total / games for total in totals] for stat, totals in total_stats.items()}

    return render(request, 'stats/index.html', {'data': avg_stats})
