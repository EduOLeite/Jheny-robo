import cloudscraper
from bs4 import BeautifulSoup
import requests

def buscar_produtos_ml(query, limit=5):
    query_formatada = query.strip().replace(" ", "-")
    url_site = f"https://lista.mercadolivre.com.br/{query_formatada}"
    
    # Instancia o scraper que desvia do Cloudflare (evita erro 403)
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    try:
        response = scraper.get(url_site, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            itens = soup.find_all('li', class_='ui-search-layout__item')
            
            # Se a estrutura antiga não retornar, tenta seletores alternativos do ML
            if not itens:
                itens = soup.select('.poly-card') or soup.select('ol.ui-search-layout > li')
                
            resultados = []
            for item in itens[:limit]:
                # Título
                titulo_elem = item.select_one('.ui-search-item__title') or item.select_one('.poly-component__title')
                titulo = titulo_elem.text.strip() if titulo_elem else "Produto Mercado Livre"
                
                # Link
                link_elem = item.select_one('a.ui-search-link') or item.select_one('a.poly-component__title') or item.find('a', href=True)
                link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else "#"
                
                # Preço
                preco_elem = item.select_one('.andes-money-amount__fraction') or item.select_one('.price-tag-fraction')
                preco_str = preco_elem.text.replace('.', '').strip() if preco_elem else "0"
                try:
                    preco = float(preco_str)
                except ValueError:
                    preco = 0.0
                
                # Imagem
                img_elem = item.find('img')
                img_url = ""
                if img_elem:
                    img_url = img_elem.get('data-src') or img_elem.get('src') or ""

                resultados.append({
                    'title': titulo,
                    'permalink': link,
                    'price': preco,
                    'thumbnail': img_url
                })
                
            if resultados:
                return resultados, None
            
        # Fallback usando API interna de sugestões
        url_api_alt = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit={limit}"
        res_api = requests.get(url_api_alt, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if res_api.status_code == 200:
            return res_api.json().get('results', []), None
            
        return [], f"Não foi possível extrair produtos para o termo '{query}'."

    except Exception as e:
        return [], f"Erro ao acessar Mercado Livre: {str(e)}"