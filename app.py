import streamlit as st
import requests

st.title("Painel de Promoções - Jheny Achadinhos")
st.write("Busque promoções reais e envie direto para o canal do Telegram!")

# Lendo credenciais seguras do Secrets
CLIENT_ID = st.secrets.get("MERCADO_LIVRE_CLIENT_ID")
CLIENT_SECRET = st.secrets.get("MERCADO_LIVRE_CLIENT_SECRET")

@st.cache_data(ttl=21000)
def get_access_token():
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def buscar_produtos(query, limit=5):
    token = get_access_token()
    if not token:
        st.error("Erro ao autenticar com a API do Mercado Livre. Verifique as credenciais.")
        return []

    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit={limit}"
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        st.error(f"Erro na busca: {response.status_code}")
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
        produtos = buscar_produtos(termo, qtd)
        
        if produtos:
            st.success(f"Encontrados {len(produtos)} produtos!")
            for item in produtos:
                st.markdown("---")
                st.subheader(item.get('title'))
                st.write(f"**Preço:** R$ {item.get('price'):.2f}")
                st.write(f"[Ver no Mercado Livre]({item.get('permalink')})")
        else:
            st.warning("Nenhum produto encontrado.")