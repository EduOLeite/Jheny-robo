import requests

def buscar_produtos_ml(query, limit=5):
    query_formatada = query.strip().replace(" ", "%20")
    
    # Endpoint alternativo com suporte a CORS e permissao publica
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query_formatada}&limit={limit}&sort=relevance"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0"
    }
    
    session = requests.Session()
    
    try:
        response = session.get(url, headers=headers, timeout=12)
        
        if response.status_code == 200:
            dados = response.json()
            return dados.get('results', []), None
        
        # Caso o IP do Streamlit sofra bloqueio 403, tenta buscar pela rota publica de itens por categoria
        elif response.status_code == 403:
            url_cat = f"https://api.mercadolibre.com/domain_discovery/search?q={query_formatada}"
            res_cat = session.get(url_cat, headers=headers, timeout=10)
            
            if res_cat.status_code == 200 and len(res_cat.json()) > 0:
                cat_id = res_cat.json()[0].get('category_id')
                url_items = f"https://api.mercadolibre.com/sites/MLB/search?category={cat_id}&limit={limit}"
                res_items = session.get(url_items, headers=headers, timeout=10)
                
                if res_items.status_code == 200:
                    return res_items.json().get('results', []), None
            
            return [], "Bloqueio temporario de IP do servidor. Tente novamente em alguns segundos ou pesquise outro termo."
        else:
            return [], f"Erro na API (HTTP {response.status_code})"
            
    except Exception as e:
        return [], f"Erro de conexão: {str(e)}"