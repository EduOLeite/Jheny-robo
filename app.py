import streamlit as st
from bot_telegram import enviar_mensagem
from buscador import buscar_produtos_mercado_livre

st.set_page_config(page_title="Jheny Achadinhos - Painel", page_icon="🛍️", layout="wide")

st.title("🛍️ Painel de Promoções - Jheny Achadinhos")
st.write("Busque promoções reais e envie direto para o canal do Telegram!")

st.divider()

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    termo_busca = st.text_input("O que você quer buscar hoje?", "smartwatch")

with col2:
    loja = st.selectbox("Selecione a Plataforma:", ["Mercado Livre", "Shopee (Em breve)"])

with col3:
    quantidade = st.slider("Qtd de Produtos:", min_value=1, max_value=10, value=3)

# Ao clicar no botão de buscar
if st.button("🔍 Buscar Promoções"):
    with st.spinner("Buscando produtos no Mercado Livre..."):
        res = buscar_produtos_mercado_livre(termo_busca, limite=quantidade)
        if res:
            st.session_state["produtos"] = res
            st.success(f"Encontrados {len(res)} produtos!")
        else:
            st.error("Nenhum produto foi encontrado. Tente mudar o termo de busca.")

st.divider()

# Exibição dos resultados e botão de envio
if "produtos" in st.session_state and st.session_state["produtos"]:
    st.subheader("Resultados da Busca:")
    
    for idx, prod in enumerate(st.session_state["produtos"]):
        col_img, col_info, col_btn = st.columns([1, 3, 1])
        
        with col_img:
            st.image(prod["imagem"], width=120)
            
        with col_info:
            st.markdown(f"### {prod['titulo']}")
            st.markdown(f"De: ~R$ {prod['preco_original']:.2f}~  👉  **Por: R$ {prod['preco_promo']:.2f}**")
            st.caption(f"Link: {prod['link_original']}")
            
        with col_btn:
            if st.button(f"🚀 Enviar no Telegram", key=f"btn_{idx}"):
                msg = (
                    f"🔥 *OFERTA IMPERDÍVEL ENCONTRADA!*\n\n"
                    f"📦 *{prod['titulo']}*\n"
                    f"❌ De: R$ {prod['preco_original']:.2f}\n"
                    f"✅ *Por apenas: R$ {prod['preco_promo']:.2f}*\n\n"
                    f"🛒 *Compre aqui:* {prod['link_original']}"
                )
                resposta = enviar_mensagem(msg)
                if resposta.get("ok"):
                    st.toast("✅ Promoção enviada para o Telegram!", icon="🎉")
                else:
                    st.error("Erro ao enviar mensagem para o Telegram.")
        st.divider()