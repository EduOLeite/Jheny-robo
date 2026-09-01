import requests
import streamlit as st

def obter_access_token():
    # Tenta ler do Streamlit Secrets (produção) ou de variáveis locais
    client_id = st.secrets.get("MERCADO_LIVRE_CLIENT_ID")
    client_secret = st.secrets.get("MERCADO_LIVRE_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        return None, "Chaves de API não encontradas nas configurações de Secrets."

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
            return None, f"Falha na autenticação (HTTP {response.status_code}): {response.text}"
    except Exception as e:
        return None, f"Erro de conexão na autenticação: {str(e)}"

def buscar_produtos_ml(query, limit=5):
    token, erro_auth = obter_access_token()
    
    # Se falhar o token com credenciais, tenta requisição direta com User-Agent
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    else:
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit={limit}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            return dados.get('results', []), None
        else:
            msg_erro = f"Erro na busca (HTTP {response.status_code})"
            if erro_auth:
                msg_erro += f" | Detalhe Auth: {erro_auth}"
            return [], msg_erro
    except Exception as e:
        return [], f"Erro de conexão ao buscar produtos: {str(e)}"