# auth.py

import requests
import streamlit as st
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://flask-app:5000/auth"  

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None
    st.session_state['username'] = None
    st.session_state['user_type'] = None
    st.session_state['store'] = None


def login(username, password):
    login_url = f"{BASE_URL}/login"
    response = requests.post(login_url, json={"username": username, "password": password})
    
    if response.status_code == 200:
        st.session_state['access_token'] = response.json().get("access_token")
        st.success("Login bem-sucedido!")
        
        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
        user_info = requests.get(f"{BASE_URL}/me", headers=headers).json()
        
        st.session_state['username'] = user_info.get("username")
        st.session_state['user_type'] = user_info.get("user_type")
        st.session_state['store'] = user_info.get("store")
    else:
        st.error("Credenciais inválidas, tente novamente.")

def register(username, password, user_type, store):
    register_url = f"{BASE_URL}/register"
    response = requests.post(register_url, json={
        "username": username,
        "password": password,
        "user_type": user_type,
        "store": store
    })

    if response.status_code == 201:
        st.success("Usuário registrado com sucesso!")
    else:
        st.error("Erro ao registrar usuário. Verifique os dados e tente novamente.")

def logout():
    st.session_state['access_token'] = None
    st.session_state['username'] = None
    st.session_state['user_type'] = None
    st.session_state['store'] = None

