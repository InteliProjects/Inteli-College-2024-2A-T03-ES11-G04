import streamlit as st
from auth.auth import login, register

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None
    st.session_state['username'] = None
    st.session_state['user_type'] = None
    st.session_state['store'] = None

st.title("Autenticação de Usuário")

tab1, tab2 = st.tabs(["Login", "Registrar"])

with tab1:
    st.subheader("Login")

    username = st.text_input("Nome de Usuário", key="login_username")
    password = st.text_input("Senha", type="password", key="login_password")
    login_button = st.button("Login")

    if login_button:
        if username and password:
            login(username, password)
        else:
            st.error("Por favor, preencha todos os campos para fazer login.")

with tab2:
    st.subheader("Registrar Novo Usuário")

    new_username = st.text_input("Nome de Usuário", key="register_username")
    new_password = st.text_input("Senha", type="password", key="register_password")
    user_type = st.selectbox("Tipo de Usuário", ["Gerente", "Vendedor", "Diretoria"], key="register_user_type")
    store = st.text_input("Loja", key="register_store")

    register_button = st.button("Registrar")

    if register_button:
        if new_username and new_password and user_type and store:
            st.write(f"Registrando usuário: {new_username} {user_type} da loja {store}")
            register(new_username, new_password, user_type, store)
        else:
            st.error("Todos os campos são obrigatórios para registrar um novo usuário.")

if st.session_state['access_token']:
    st.sidebar.success(f"Usuário logado: {st.session_state['username']}")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({'access_token': None, 'username': None, 'user_type': None, 'store': None}))
