-- Remove tabelas existentes para garantir um ambiente limpo (ideal para teste, nesse caso o teste técnico)
DROP TABLE IF EXISTS vendas;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS fornecedores;

-- Tabela de Fornecedores
CREATE TABLE fornecedores (
    id SERIAL PRIMARY KEY,
    nome_empresa VARCHAR(100) NOT NULL,
    contato VARCHAR(100),
    telefone VARCHAR(20)
);

-- Tabela de Clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefone VARCHAR(20)
);

-- Tabela de produtos
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(50),
    estoque INT DEFAULT 0,
    fornecedor_id INT, 
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id) 
);

-- Tabela de vendas
CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    produto_id INT,
    cliente_id INT, 
    quantidade INT NOT NULL,
    data_venda TIMESTAMP DEFAULT NOW(),
    valor_total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) 
);