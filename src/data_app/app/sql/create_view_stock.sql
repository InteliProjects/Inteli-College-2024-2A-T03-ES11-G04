CREATE OR REPLACE VIEW view_stock AS
SELECT 
    JSONExtractString(line_data, 'cod_loja') AS cod_loja, 
    CAST(JSONExtract(line_data, 'cod_prod', 'UInt64') AS BIGINT) AS cod_prod, 
    CAST(JSONExtract(line_data, 'quantidade', 'Int32') AS INT) AS quantidade
FROM working_data 
WHERE tag = 'daily_stock_dataset';