SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL,
        descricao VARCHAR(1000) NOT NULL,
        preco REAL NOT NULL,
        estoque INTEGER NOT NULL);
"""

SQL_INSERIR = """
    INSERT INTO produto (nome, descricao, preco, estoque) 
    VALUES (?, ?, ?, ?);
"""

SQL_ALTERAR = """
    UPDATE produto 
    SET nome = ?, descricao = ?, preco = ?, estoque = ? 
    WHERE id = ?;
"""

SQL_EXCLUIR = """
    DELETE FROM produto 
    WHERE id = ?;
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, descricao, preco, estoque 
    FROM produto 
    WHERE id = ?;
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, descricao, preco, estoque 
    FROM produto 
    ORDER BY nome;
"""