import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from services.logging_service import send_log_to_elasticsearch
from services.clickhouse_client_service import fetch_sku_data, fetch_stock_data
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sugerir_substituto_com_estoque(cod_prod_informado, cod_loja):
    log_message = []
    status_code = 500  

    try:
        logger.info("Carregando datasets de SKU e estoque via API.")
        log_message.append("Carregando datasets de SKU e estoque via API. \n")
        
        df_produtos = fetch_sku_data() 
        df_estoque = fetch_stock_data()  

        if df_produtos is None or df_estoque is None:
            raise ValueError("Um ou mais datasets não foram encontrados.")

        logger.info(f"Primeiros registros de df_produtos: {df_produtos.head()}")
        logger.info(f"Primeiros registros de df_estoque: {df_estoque.head()}")

        logger.info(f"Buscando produto com código {cod_prod_informado} no dataset.")
        try:
            cod_prod_informado = int(cod_prod_informado)  
        except ValueError:
            logger.warning(f"Formato de código de produto inválido: {cod_prod_informado}")
            return "Código de produto inválido"

        produto_info = df_produtos[df_produtos['cod_prod'] == cod_prod_informado]
        logger.info(f"Resultado da busca do produto: {produto_info}")

        if produto_info.empty:
            logger.warning(f"Produto com código {cod_prod_informado} não encontrado.")
            log_message.append(f"Produto com código {cod_prod_informado} não encontrado. \n")
            status_code = 404  
            return "Produto não encontrado"

        categoria = produto_info['categoria'].values[0]
        subcategoria = produto_info['sub_categoria'].values[0]
        valor_ref = pd.to_numeric(produto_info['conteudo_valor'], errors='coerce').values[0]
        conteudo_medida_ref = produto_info['conteudo_medida'].values[0]
        descricao = produto_info['descricao'].values[0]

        if np.isnan(valor_ref):
            logger.warning(f"Conteúdo valor do produto {cod_prod_informado} não é numérico ou está faltando.")
            log_message.append(f"Conteúdo valor do produto {cod_prod_informado} não é numérico ou está faltando. \n")
            status_code = 400 
            return "Conteúdo valor não é numérico ou está faltando"

        logger.info(f"Produto {cod_prod_informado} encontrado: {descricao}, categoria: {categoria}, subcategoria: {subcategoria}.")
        log_message.append(f"Produto {cod_prod_informado} encontrado com sucesso. \n")

        produtos_potenciais = df_produtos[
            (df_produtos['categoria'] == categoria) &
            (df_produtos['sub_categoria'] == subcategoria) &
            pd.to_numeric(df_produtos['conteudo_valor'], errors='coerce').between(valor_ref * 0.9, valor_ref * 1.1) &
            (df_produtos['conteudo_medida'] == conteudo_medida_ref) &
            (df_produtos['cod_prod'] != cod_prod_informado)
        ].copy()

        if produtos_potenciais.empty:
            logger.info(f"Nenhum produto substituto encontrado para o produto {cod_prod_informado}.")
            log_message.append(f"Nenhum produto substituto encontrado para o produto {cod_prod_informado}. \n")
            status_code = 404
            return "Nenhum produto substituto encontrado"

        def remove_stop_words(text):
            stop_words = set(["de", "o", "a", "e", "que", "do", "da", "em", "um", "para", "com", "não", "uma", "os", "no"])
            words = text.lower().split()
            return ' '.join([word for word in words if word not in stop_words])

        descricoes = [descricao] + produtos_potenciais['descricao'].fillna("").tolist()
        descricoes_sem_stopwords = [remove_stop_words(desc) for desc in descricoes]

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(descricoes_sem_stopwords)
        similaridade = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        produtos_potenciais['similaridade'] = similaridade

        produtos_potenciais = produtos_potenciais.sort_values(by='similaridade', ascending=False)

        produtos_em_estoque = pd.DataFrame()
        produtos_ja_adicionados = set()  # Set para rastrear produtos já adicionados

        for _, produto_substituto in produtos_potenciais.iterrows():
            cod_produto_substituto = produto_substituto['cod_prod']
            estoque_produto = df_estoque[
                (df_estoque['cod_loja'] == cod_loja) & 
                (df_estoque['cod_prod'] == cod_produto_substituto)
            ]

            if not estoque_produto.empty and estoque_produto['quantidade'].values[0] > 0:
                # Verifique se o produto já foi adicionado
                if cod_produto_substituto not in produtos_ja_adicionados:
                    produto_substituto['preco'] = random.uniform(40.00, 60.00)  
                    produto_substituto['margem_lucro_bruto'] = random.uniform(20.0, 30.0)  
                    produtos_em_estoque = pd.concat([produtos_em_estoque, produto_substituto.to_frame().T])
                    
                    # Adicione o código do produto ao conjunto
                    produtos_ja_adicionados.add(cod_produto_substituto)

            if len(produtos_em_estoque) >= 3:
                break

        if not produtos_em_estoque.empty:
            logger.info(f"Produtos substitutos encontrados para o produto {cod_prod_informado}.")
            log_message.append(f"Produtos substitutos encontrados para o produto {cod_prod_informado}. \n")
            status_code = 200
            
            resultado = []
            for _, produto in produtos_em_estoque.iterrows():
                resultado.append({
                    "nome": produto['nome_completo'], 
                    "id": produto['cod_prod'],         
                    "descricao": produto['descricao'],
                    "preco": f"R$ {produto['preco']:.2f}",    
                    "margem": f"{produto['margem_lucro_bruto']:.2f}%" 
                })
            
            return resultado
        else:
            logger.info(f"Nenhum produto substituto disponível em estoque para o produto {cod_prod_informado}.")
            log_message.append(f"Nenhum produto substituto disponível em estoque para o produto {cod_prod_informado}. \n")
            status_code = 200
            return "Nenhum produto substituto disponível em estoque"

    except Exception as e:
        logger.error(f"Erro ao sugerir substitutos: {e}", exc_info=True)
        log_message.append(f"Erro ao sugerir substitutos: {str(e)} \n")
        status_code = 500
        raise RuntimeError(f"Erro ao sugerir substitutos: {str(e)}")
    
    finally:
        send_log_to_elasticsearch(log_message, "get_product_substitute", status_code)
