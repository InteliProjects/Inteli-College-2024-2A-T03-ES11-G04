import logging
from flask import Blueprint, jsonify, request
from services.substitutes_service import sugerir_substituto_com_estoque

# Inicializando o Blueprint para substitutos
substitute_blueprint = Blueprint('substitute', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definindo a rota para obter substitutos de produtos
@substitute_blueprint.route('/get_product_substitute', methods=['POST'])
def get_product_substitute():
    try:
        # Parsing dos dados da requisição (Código do Produto e Código da Loja)
        product_input = request.get_json()
        cod_prod_informado = product_input.get('cod_prod')
        cod_loja = product_input.get('cod_loja')

        # Validação dos dados de entrada
        if not cod_prod_informado or not cod_loja:
            return jsonify({'error': 'Código do produto ou código da loja não informado'}), 400

        # Chamando a função de serviço para obter os substitutos
        substitutos = sugerir_substituto_com_estoque(cod_prod_informado, cod_loja)

        # Verificando o resultado e retornando a resposta apropriada
        if isinstance(substitutos, str):
            return jsonify({'error': substitutos}), 404  # Retorna 404 se nenhum substituto for encontrado

        # Se for uma lista, retornar diretamente
        if isinstance(substitutos, list):
            result = substitutos  
        else:
            # Se for um DataFrame ou similar, converter para dicionário antes de retornar
            result = substitutos.to_dict(orient='records')

        return jsonify(result), 200

    except Exception as e:
        # Logar o erro no servidor
        logger.error(f"Erro no servidor: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erro interno do servidor'}), 500
