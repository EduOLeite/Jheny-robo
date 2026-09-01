import requests
import urllib.parse

def buscar_produtos_ml(query, limit=5):
    # Formata o texto para padrão de link (ex: "smartwatch apple" vira "smartwatch%20apple")
    query_formatada = urllib.parse.quote(query.strip())
    
    # URL oficial da API pública do Mercado Livre
    url_oficial = f"https://api.mercadolibre.com/sites/MLB/search?q={query_formatada}&limit={limit}"
    
    # Passa a URL pelo proxy gratuito AllOrigins para evitar o bloqueio de IP (erro 403) do Streamlit Cloud
    url_proxy = f"https://api.allorigins.win/raw?url={urllib.parse.quote(url_oficial)}"
    
    try:
        response = requests.get(url_proxy, timeout=15)
        
        if response.status_code == 200:
            dados = response.json()
            resultados = dados.get('results', [])
            
            if not resultados:
                return [], f"Nenhum produto encontrado para '{query}'."
                
            return resultados, None
        else:
            return [], f"Erro na API via proxy (HTTP {response.status_code})"
            
    except Exception as e:
        return [], f"Falha de conexão com a busca: {str(e)}"