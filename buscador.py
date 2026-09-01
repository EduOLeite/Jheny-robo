import requests
import urllib.parse

def buscar_produtos_ml(query, limit=5):
    query_formatada = urllib.parse.quote(query.strip())
    url_oficial = f"https://api.mercadolibre.com/sites/MLB/search?q={query_formatada}&limit={limit}"
    
    # Lista de rotas para garantir que a busca funcione sem travar
     proxies = [
        # Proxy 1: Corsproxy (Alta velocidade)
        f"https://corsproxy.io/?{urllib.parse.quote(url_oficial)}",
        # Proxy 2: Thingproxy (Estável)
        f"https://thingproxy.freeboard.io/fetch/{url_oficial}",
        # Rota Direta com User-Agent
        url_oficial
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    for url in proxies:
        try:
            response = requests.get(url, headers=headers, timeout=6)
            
            if response.status_code == 200:
                dados = response.json()
                resultados = dados.get('results', [])
                
                if resultados:
                    return resultados, None
        except Exception:
            continue  # Se um proxy falhar ou der timeout, pula para o próximo
            
    return [], f"Não foi possível obter produtos para '{query}'. Tente novamente."