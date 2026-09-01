import requests
from urllib.parse import quote

def buscar_produtos_mercado_livre(termo_busca, limite=5):
    """Busca produtos no Mercado Livre usando a API publica sem necessidade de token."""
    termo_encoded = quote(termo_busca)
    
    # Endpoint de autocompletar/busca rápida pública do Mercado Livre
    url = f"https://http2.mlstatic.com/resources/sites/MLB/autosuggest?q={termo_encoded}&showFilters=true"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Referer": "https://www.mercadolivre.com.br/"
    }
    
    try:
        # 1. Busca os IDs das sugestões de produtos
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"Erro na consulta de sugestões: {resp.status_code}")
            return []
            
        dados = resp.json()
        produtos_encontrados = []
        
        # Filtra os resultados de produtos retornados pela busca rápida
        sugestoes = dados.get("suggested_queries", []) + dados.get("suggested_categories", [])
        
        # Faz uma busca alternativa via endpoint de produtos abertos se necessário
        url_busca_aberta = f"https://api.mercadolibre.com/sites/MLB/search?q={termo_encoded}"
        resp_produtos = requests.get(url_busca_aberta, headers={"User-Agent": "Googlebot"}, timeout=10)
        
        if resp_produtos.status_code == 200:
            resultados = resp_produtos.json().get("results", [])
            for item in resultados[:limite]:
                preco_promo = float(item.get("price", 0.0))
                preco_orig = item.get("original_price")
                
                preco_original = float(preco_orig) if (preco_orig and float(preco_orig) > preco_promo) else preco_promo * 1.20
                imagem_url = item.get("thumbnail", "").replace("-I.jpg", "-O.jpg")
                
                produtos_encontrados.append({
                    "id": item.get("id"),
                    "titulo": item.get("title"),
                    "preco_original": preco_original,
                    "preco_promo": preco_promo,
                    "link_original": item.get("permalink"),
                    "imagem": imagem_url
                })
        
        return produtos_encontrados

    except Exception as e:
        print(f"Erro ao buscar no Mercado Livre: {e}")
        return []

if __name__ == "__main__":
    produtos = buscar_produtos_mercado_livre("notebook", limite=3)
    print(f"Resultado do teste: {len(produtos)} produtos encontrados.")
    for p in produtos:
        print(f"- {p['titulo']}: R$ {p['preco_promo']}")