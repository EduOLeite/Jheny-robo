import requests

def buscar_produtos_ml(query, limit=5):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit={limit}"
    
    # Header simulando navegador para evitar bloqueio 403
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            return dados.get('results', []), None
        else:
            return [], f"Erro na API do Mercado Livre (Código HTTP {response.status_code}): {response.text}"
            
    except Exception as e:
        return [], f"Falha ao conectar com o Mercado Livre: {str(e)}"