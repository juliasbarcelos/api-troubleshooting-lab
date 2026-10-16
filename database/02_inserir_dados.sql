USE api_troubleshooting_lab;

INSERT INTO pedidos
    (cliente, produto, quantidade, estado)
VALUES
    ('Cliente Teste', 'Notebook', 1, 'pendente'),
    ('Maria Silva', 'Monitor', 2, 'enviado'),
    ('Joao Santos', 'Teclado', 3, 'entregue'),
    ('Ana Costa', 'Rato Wireless', 1, 'pendente'),
    ('Pedro Almeida', 'Impressora', 1, 'cancelado');

SELECT
    id,
    cliente,
    produto,
    quantidade,
    estado,
    data_criacao
FROM pedidos
ORDER BY id;