CREATE OR REPLACE VIEW view_sku_dataset AS
SELECT 
    JSONExtractString(line_data, 'categoria') AS categoria,
    JSONExtractString(line_data, 'sub_categoria') AS sub_categoria,
    JSONExtractString(line_data, 'marca') AS marca,
    CAST(JSONExtract(line_data, 'conteudo_valor', 'Float64') AS DECIMAL(10, 2)) AS conteudo_valor,
    JSONExtractString(line_data, 'conteudo_medida') AS conteudo_medida,
    JSONExtractInt(line_data, 'cod_prod') AS cod_prod,
    JSONExtractString(line_data, 'nome_abrev') AS nome_abrev,
    JSONExtractString(line_data, 'nome_completo') AS nome_completo,
    JSONExtractString(line_data, 'descricao') AS descricao
FROM working_data
WHERE tag = 'sku_dataset';
