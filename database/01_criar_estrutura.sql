-- Projeto 3: API Troubleshooting Lab
-- Script 01: Criação da estrutura MySQL
-- Base de dados para simulação de pedidos fictícios

CREATE DATABASE IF NOT EXISTS api_troubleshooting_lab;

USE api_troubleshooting_lab;

-- Tabela de pedidos

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    produto VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'pendente',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_quantidade_positiva CHECK (quantidade > 0)
);

-- Verificação da estrutura

SHOW TABLES;
DESCRIBE pedidos;
