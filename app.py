import streamlit as st
import requests

st.set_page_config(page_title="Painel Jheny Achadinhos", layout="wide")

st.title("🛍️ Painel de Promoções - Jheny Achadinhos")
st.write("Busque promoções reais e envie direto para o canal do Telegram!")

# Lendo credenciais seguras do Secrets
CLIENT_ID = st.secrets.get("MERCADO_LIVRE_CLIENT_ID")
CLIENT_SECRET = st.secrets.get("MERCADO_LIVRE_CLIENT_SECRET")

def buscar_produtos_ml(query, limit=5):
    # Endpoint público de busca de produtos no Brasil (MLB)
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit={limit}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        dados = response.json()
        return dados.get('results', [])
    else:
        st.error(f"Erro na API do Mercado Livre (Código {response.status_code})")
        return []

# Interface do Usuário
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    termo = st.text_input("O que você quer buscar hoje?", "smartwatch")
with col2:
    plataforma = st.selectbox("Selecione a Plataforma:", ["Mercado Livre"])
with col3:
    qtd = st.slider("Qtd de Produtos:", 1, 10, 3)

if st.button("🔍 Buscar Promoções"):
    with st.spinner("Buscando ofertas..."):
        produtos = buscar_produtos_ml(termo, qtd)
        
        if produtos:
            st.success(f"Encontrados {len(produtos)} produtos!")
            for item in produtos:
                st.markdown("---")
                col_img, col_info = st.columns([1, 3])
                
                with col_img:
                    if item.get('thumbnail'):
                        # Melhora a resolução da imagem do Mercado Livre
                        img_url = item.get('thumbnail').replace("-I.jpg", "-O.jpg")
                        st.image(img_url, width=150)
                        
                with col_info:
                    st.subheader(item.get('title'))
                    preco = item.get('price', 0)
                    st.write(f"💰 **Preço:** R$ {preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                    st.markdown(f"🔗 [Ver Oferta no Mercado Livre]({item.get('permalink')})")
        else:
            st.error("Nenhum produto foi encontrado. Tente mudar o termo de busca.")