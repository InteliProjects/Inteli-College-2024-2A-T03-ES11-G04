import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from services.view_service import fetch_data

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = None

if st.session_state.get('user_type') == 'Gerente' or st.session_state.get('user_type') == 'Diretoria':
    st.title("Desempenho da loja")

    store_id_input = st.text_input("Digite o ID da loja (ex: RJ_37):")
    store_id = store_id_input.strip().upper() 

    mes = st.selectbox("Selecione o mês", ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
    mes_dict = {
        'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
        'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
        'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
    }
    mes_selecionado = mes_dict[mes]

    ano = st.selectbox("Selecione o ano", [2022, 2023, 2024])

    def filter_remuneracao(store_id, mes, ano):
        endpoint = "remuneracao"
        df = fetch_data(endpoint)
        df_filtrado = df[(df['t.cod_loja'] == store_id) & (df['t.mes'] == mes) & (df['t.ano'] == ano)]
        return df_filtrado

    if st.button("Buscar Desempenho"):
        if store_id and mes_selecionado and ano:
            df_remuneracao = filter_remuneracao(store_id, mes_selecionado, ano)

            if not df_remuneracao.empty:
                total_vendas = df_remuneracao['total_vendas'].values[0]
                target = df_remuneracao['target'].values[0]

                desempenho_loja = pd.DataFrame({
                    'Métrica': ['Vendas Realizadas', 'Meta do Mês'],
                    'Valor': [total_vendas, target]
                })

                fig = px.bar(
                    desempenho_loja, 
                    x='Valor', 
                    y='Métrica', 
                    text_auto=True,  
                    orientation='h',  
                    color='Métrica',
                    color_discrete_map={'Vendas Realizadas': '#1f77b4', 'Meta do Mês': '#FFD700'}  # Azul para vendas, dourado para meta
                )

                fig.update_layout(
                    title=f'Desempenho de Vendas da Loja {store_id}',
                    xaxis_title='Valor (R$)',
                    yaxis_title='',
                    showlegend=False
                )

                st.plotly_chart(fig)

                if 'l.regiao' in df_remuneracao.columns:
                    region = df_remuneracao['l.regiao'].values[0]
                    df_regiao = fetch_data("remuneracao")
                    df_regiao_filtrado = df_regiao[(df_regiao['l.regiao'] == region) & (df_regiao['t.mes'] == mes_selecionado) & (df_regiao['t.ano'] == ano)]
                    df_regiao_filtrado['atingimento'] = df_regiao_filtrado['total_vendas'] / df_regiao_filtrado['target']
                    df_regiao_filtrado = df_regiao_filtrado.sort_values('atingimento', ascending=False).reset_index()

                    posicao_loja = df_regiao_filtrado[df_regiao_filtrado['t.cod_loja'] == store_id].index[0] + 1

                    st.markdown(f"<div style='border: 1px solid #ddd; padding: 10px; border-radius: 5px; background-color: #262730; color: white;'>"
                            f"<strong>Você vendeu R$ {total_vendas:,.2f} até o momento</strong></div>", unsafe_allow_html=True)

                    st.write("")

                    st.markdown(f"<div style='border: 1px solid #ddd; padding: 10px; border-radius: 5px; background-color: #262730; color: white;'>"
                                f"<strong>Você está em {posicao_loja}º lugar em maior atingimento de meta entre as lojas da sua região</strong></div>", unsafe_allow_html=True)

                # Projeção de vendas com base nos dados de 2022 e 2023
                df_anos_anteriores = df_regiao[(df_regiao['t.ano'] != ano)]
                
                # Usando média de vendas mensais
                df_anos_anteriores = df_anos_anteriores.groupby(['t.mes']).agg({'total_vendas': 'mean'}).reset_index()

                X = df_anos_anteriores['t.mes'].values.reshape(-1, 1)
                y = df_anos_anteriores['total_vendas'].values

                # Ajuste do modelo de regressão polinomial (grau 2)
                poly = PolynomialFeatures(degree=2)
                X_poly = poly.fit_transform(X)

                model = LinearRegression()
                model.fit(X_poly, y)

                # Projeção para o ano selecionado (meses de 1 a 12)
                meses_para_projecao = np.array(range(1, 13)).reshape(-1, 1)
                meses_para_projecao_poly = poly.transform(meses_para_projecao)
                projecao_vendas = model.predict(meses_para_projecao_poly)

                df_projecao = pd.DataFrame({
                    'Mes': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
                    'Vendas Projetadas': projecao_vendas
                })

                # Criando o gráfico com o floor em 0 no eixo y
                fig_projecao = px.line(df_projecao, x='Mes', y='Vendas Projetadas', markers=True)
                fig_projecao.update_layout(
                    title=f'Projeção de Vendas para 2024 (Loja {store_id})',
                    xaxis_title='Meses',
                    yaxis_title='Vendas Projetadas (R$)',
                    yaxis=dict(range=[0, df_projecao['Vendas Projetadas'].max() + 1000])  # Define o eixo y começando em 0
                )
                st.plotly_chart(fig_projecao)

    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
elif st.session_state.get('user_type') == 'Vendedor':
        st.error("Acesso negado. Apenas gerentes e diretores podem acessar esta página.")
elif st.session_state['access_token'] is None:
    st.error("Você precisa estar logado para acessar esta página.")
