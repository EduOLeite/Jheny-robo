import requests

def buscar_produtos_ml(query, limit=5):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit={limit}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            resultados = dados.get('results', [])
            return resultados, None
        else:
            return [], f"Erro na busca (HTTP {response.status_code})"
            
    except Exception as e:
        return [], f"Falha de conexão: {str(e)}"