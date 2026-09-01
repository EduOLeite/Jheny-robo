import requests
import streamlit as st

def obter_access_token():
    client_id = str(st.secrets.get("MERCADO_LIVRE_CLIENT_ID", "")).strip()
    client_secret = str(st.secrets.get("MERCADO_LIVRE_CLIENT_SECRET", "")).strip()
    
    if not client_id or not client_secret:
        return None, "Credenciais não encontradas no Secrets do Streamlit."

    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get('access_token'), None
        else:
            return None, f"Erro OAuth ({response.status_code}): {response.text}"
    except Exception as e:
        return None, f"Erro de conexão na autenticação: {str(e)}"

def buscar_produtos_ml(query, limit=5):
    token, erro_token = obter_access_token()
    
    if not token:
        return [], f"Falha ao obter token de acesso: {erro_token}"

    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit={limit}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            return dados.get('results', []), None
        else:
            return [], f"Erro na busca (HTTP {response.status_code}): {response.text}"
            
    except Exception as e:
        return [], f"Erro de conexão com o Mercado Livre: {str(e)}"