-- Populando Fornecedores
INSERT INTO fornecedores (nome_empresa, contato, telefone) VALUES
('Tech Imports', 'Carlos Silva', '11987654321'),
('Editora Saber', 'Beatriz Souza', '21912345678'),
('Fashion Wear Distribuidora', 'Mariana Costa', '31998761234');

-- Populando Clientes
INSERT INTO clientes (nome, email, telefone) VALUES
('João Pereira', 'joao.p@email.com', '81988887777'),
('Ana Oliveira', 'ana.o@email.com', '81999995555');

-- Populando Produtos com referência ao fornecedor (expandido para >=10 produtos)
INSERT INTO produtos (nome, preco, categoria, estoque, fornecedor_id) VALUES
('Laptop Gamer Nitro 5', 4500.00, 'Eletrônicos', 10, 1),
('Smartphone Galaxy S23', 3800.50, 'Eletrônicos', 15, 1),
('Monitor LED 24"', 899.90, 'Eletrônicos', 8, 1),
('Fone de Ouvido Bluetooth XYZ', 199.90, 'Acessórios', 50, 1),
('Geladeira Duplex 400L', 2499.00, 'Eletrodomésticos', 4, 1),
('O Senhor dos Anéis - Trilogia', 120.00, 'Livros', 20, 2),
('Duna - Frank Herbert', 55.75, 'Livros', 2, 2),
('Caderno Universitário 200 folhas', 12.50, 'Papelaria', 100, 2),
('Camisa Polo Básica', 79.90, 'Vestuário', 30, 3),
('Calça Jeans Slim', 150.00, 'Vestuário', 25, 3),
('Relógio de Pulso Unissex', 249.00, 'Acessórios', 15, 3);