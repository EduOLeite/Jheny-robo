import requests
import streamlit as st

CLIENT_ID = st.secrets.get("MERCADO_LIVRE_CLIENT_ID")
CLIENT_SECRET = st.secrets.get("MERCADO_LIVRE_CLIENT_SECRET")

@st.cache_data(ttl=18000)
def obter_access_token():
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
    except Exception:
        return None

def buscar_produtos_ml(query, limit=5):
    token = obter_access_token()
    if not token:
        return None, "Erro na autenticação com a API do Mercado Livre."

    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit={limit}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('results', []), None
    else:
        return [], f"Erro na API do Mercado Livre (Código {response.status_code})"