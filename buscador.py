import requests

def buscar_produtos_ml(query, limit=5):
    # Formata a busca para URL válida
    query_formatada = query.strip().replace(" ", "%20")
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query_formatada}&limit={limit}"
    
    # Cabecalho para simular acesso de integrador autenticado via cliente web
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "pt-BR,pt;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            resultados = dados.get('results', [])
            return resultados, None
        elif response.status_code == 403:
            # Fallback para rota de itens em destaque/catálogo em caso de 403 do IP
            url_alt = f"https://api.mercadolibre.com/sites/MLB/search?q={query_formatada}&limit={limit}&status=active"
            res_alt = requests.get(url_alt, headers=headers, timeout=10)
            if res_alt.status_code == 200:
                return res_alt.json().get('results', []), None
            return [], "Servidor temporariamente bloqueado pelo Mercado Livre (403). Tente novamente em alguns instantes."
        else:
            return [], f"Erro na API do Mercado Livre (Código {response.status_code})"
            
    except Exception as e:
        return [], f"Falha de conexão com o Mercado Livre: {str(e)}"