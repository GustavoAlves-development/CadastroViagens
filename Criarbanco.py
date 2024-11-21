import sqlite3

banco = sqlite3.connect('../../Downloads/CadastroViagens-main/CadastroViagens-main/Viajens.db')
cursor = banco.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Usuarios(
        id INTEGER PRIMARY KEY,
        Login TEXT UNIQUE,
        Senha TEXT
);
''')