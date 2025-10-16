-- 1. Produtos com estoque maior que 5, ordenados por categoria e preço
SELECT
    id,
    nome,
    categoria,
    preco,
    estoque
FROM produtos
WHERE estoque > 5
ORDER BY categoria, preco;

-- 2. Relatório de vendas com nome do produto, categoria e data
-- Esta consulta é a base para a função get_all() no VendaModel
SELECT
    v.id AS venda_id,
    p.nome AS produto,
    p.categoria,
    c.nome AS cliente,
    v.quantidade,
    v.valor_total,
    v.data_venda
FROM vendas v
JOIN produtos p ON v.produto_id = p.id
JOIN clientes c ON v.cliente_id = c.id;

-- 3. Total de vendas e receita por categoria nos últimos 30 dias
SELECT
    p.categoria,
    COUNT(v.id) AS total_de_vendas,
    SUM(v.valor_total) AS receita_total
FROM vendas v
JOIN produtos p ON v.produto_id = p.id
WHERE v.data_venda >= NOW() - INTERVAL '30 days'
GROUP BY p.categoria
ORDER BY receita_total DESC;

-- 4. Top 5 produtos mais vendidos por quantidade
SELECT
    p.nome,
    SUM(v.quantidade) AS quantidade_total_vendida
FROM vendas v
JOIN produtos p ON v.produto_id = p.id
GROUP BY p.nome
ORDER BY quantidade_total_vendida DESC
LIMIT 5;

-- 5. Produtos nunca vendidos ou com estoque crítico (< 3 unidades)
SELECT
    id,
    nome,
    estoque,
    CASE
        WHEN id NOT IN (SELECT DISTINCT produto_id FROM vendas) THEN 'Nunca Vendido'
        WHEN estoque < 3 THEN 'Estoque Crítico'
    END AS status
FROM produtos
WHERE id NOT IN (SELECT DISTINCT produto_id FROM vendas)
   OR estoque < 3;