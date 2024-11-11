import streamlit as st
from services.subs_service import get_substitute_products

if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = None

if st.session_state.get('user_type') == 'Diretoria' or st.session_state.get('user_type') == 'Gerente' or st.session_state.get('user_type') == 'Vendedor':
    st.title("Desempenho da loja")

    st.markdown("""
        <style>
        /* Botão de envio */
        .stButton button {
            width: 100%;
            background-color: #FF4B4B;
            color: white;
            border-radius: 5px;
        }

        .stButton button:hover {
            background-color: #FF3333; /* Cor do botão ao passar o mouse */
            color: white; /* Cor do texto permanece branca ao dar hover */
        }

        /* Caixa de informações do produto informado */
        .product-info-box {
            background-color: #1e3a5f;
            padding: 15px;
            border-radius: 8px;
            color: #d4d8e4;
            font-size: 16px;
            margin-top: 20px;
            margin-bottom: 20px;
        }

        /* Título do produto */
        .product-name {
            font-weight: bold;
            font-size: 20px;
            color: #d4d8e4;
        }

        /* Preço e margem */
        .product-price, .product-margin {
            color: #32B950;
            font-weight: bold;
        }

        /* Descrição do produto */
        .product-description {
            margin-top: 10px;
            color: #a0a0a0;
            font-size: 14px;
        }

        /* Estilização da sugestão de produtos */
        div.product-card {
            border: 1px solid #3a3b3c;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            background-color: #262730;
        }

        h4.product-name {
            font-weight: bold;
            color: #d4d8e4;
            font-size: 18px;
        }

        p.product-price, p.product-margin {
            color: #32B950;
            font-weight: bold;
        }

        /* Caixa de informações de Cross-Sell */
        .blue-info-box {
            background-color: #1e3a5f;
            padding: 10px;
            border-radius: 8px;
            color: #d4d8e4;
            font-size: 14px;
            border-left: 5px solid #5d9ce5;
            margin-bottom: 20px;
        }

        /* Caixa de input */
        .css-1lcbmhc {
            background-color: #262730 !important;
            color: white !important;
        }

        /* Centralizando o dropdown */
        .css-1lcbmhc {
            text-align: center;
        }

        </style>
    """, unsafe_allow_html=True)

    # Título da Página
    st.title("Sugestão de produtos substitutos")
    st.write("Informe o ID de um produto da compra para receber sugestão de um produto a ser vendido em conjunto, ou de um produto substituto.")

    # Caixa de informações para Cross-Sell e substitutos
    st.markdown("""
    <div class="blue-info-box">
        <p>💡 <strong>Para cross-sell</strong>, são considerados os produtos mais vendidos em conjunto. 
        <strong>Para produtos substitutos</strong>, são consideradas características do produto, disponibilidade em estoque e valor.</p>
    </div>
    """, unsafe_allow_html=True)

    # Formulário de entrada para ID do produto e ID da loja
    col1 = st.columns(1)
    cod_prod = st.text_input("ID do produto", value="")


    # Preço e margem mockados
    preco_mock = "R$47,00"
    margem_mock = "29%"

    # Botão para enviar
    search = st.button("Enviar")

    # Processamento da entrada e exibição dos resultados
    if search:
        if cod_prod:
            substitutos = get_substitute_products(cod_prod)

            # Simulando a recuperação das informações do produto
            if isinstance(substitutos, list) and substitutos:
                produto_informado = substitutos[0]
                produto_nome = produto_informado.get('nome', 'Produto sem nome')
                descricao = produto_informado.get('descricao', 'Descrição indisponível')
                codigo_produto = produto_informado.get('id', 'ID não disponível')

                # # Exibindo o produto informado
                # st.markdown(f"""
                # <div class="product-info-box">
                #     <div class="product-name">{produto_nome} - {codigo_produto}</div>
                #     <p class="product-description">{descricao}</p>
                #     <p>Preço: <span class="product-price">{preco_mock}</span> | Margem: <span class="product-margin">{margem_mock}</span></p>
                # </div>
                # """, unsafe_allow_html=True)

                # Display product info box with mocked price and margin
                st.markdown(f"""
                <div class="product-info-box">
                    <strong>Produto informado</strong> <br>
                    {produto_nome} <br> Preço: <strong>{preco_mock}</strong> | Margem: <strong>{margem_mock}</strong> <br>
                    
                </div>
                """, unsafe_allow_html=True)

                st.subheader("Potenciais produtos substitutos:")

                # Opções de ordenação
                order_by = st.selectbox("Ordenar por", ["Margem de lucro", "Preço"])

                if order_by == "Margem de lucro":
                    substitutos = sorted(substitutos, key=lambda x: float(x.get("margem", "0").replace("%", "")), reverse=True)
                elif order_by == "Preço":
                    substitutos = sorted(substitutos, key=lambda x: float(x.get("preco", "R$ 0,00").replace("R$ ", "").replace(",", ".")), reverse=True)

                # Exibindo os produtos substitutos
                for product in substitutos:
                    st.markdown(f"""
                    <div class="product-card">
                        <h4 class="product-name">{product.get('nome', 'Sem nome')} - {product.get('id', 'Sem ID')}</h4>
                        <p>{product.get('descricao', 'Sem descrição')}</p>
                        <p>Preço: <span class="product-price">R$ {product.get('preco', '0,00')}</span> | Margem: <span class="product-margin">{product.get('margem', 'Sem margem')}</span></p>
                </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Nenhum produto substituto encontrado ou houve um erro.")
        else:
            st.error("Por favor, preencha o ID do produto.")
elif st.session_state['access_token'] is None:
    st.error("Você precisa estar logado para acessar esta página.")
