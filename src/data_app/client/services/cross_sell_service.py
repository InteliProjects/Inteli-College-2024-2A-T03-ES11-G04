import requests
import streamlit as st

API_BASE_URL = "http://flask-app:5000"

def get_similar_products(cod_prod):
    if st.session_state['store']:
        cod_loja = st.session_state['store']
    else:
        st.error("Erro: Código da loja não encontrado. Verifique se você está logado.")
        return []

    payload = {
        "cod_loja": cod_loja,  
        "cod_prod": cod_prod
    }

    try:
        response = requests.post(f"{API_BASE_URL}/get_similar_products", json=payload)

        if response.status_code == 200:
            try:
                result = response.json()

                if 'data' in result:
                    return result['data']
                else:
                    st.error("Erro: Resposta inesperada do servidor. 'data' não encontrado.")
                    return []
            except ValueError:
                st.error("Erro ao decodificar a resposta do servidor. Resposta não está em formato JSON.")
                return []
        else:
            st.error(f"Erro: {response.status_code} - {response.text}")
            return []

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao tentar se conectar ao servidor: {e}")
        return []

