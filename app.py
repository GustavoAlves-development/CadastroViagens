from flask import Flask, render_template, g, request, redirect, session, flash
import sqlite3

from Criarbanco import banco, cursor

app = Flask(__name__)
app.secret_key = 'Vinicuis'


def ligar_banco():
    banco = g._database = sqlite3.connect('Viajens.db')
    return banco


@app.teardown_appcontext
def fechar_banco(exception):
    banco = ligar_banco()
    banco.close()

@app.route('/')
def Inicial():  # put application's code here
        if 'Usuario_Logado' not in session:
            return redirect('/login')
        else:
            return render_template('index.html')


@app.route('/criar', methods=['POST', 'GET'])
def Cadastrar():
        if 'Usuario_Logado' not in session:
            return redirect('/login')
        else:
            banco = ligar_banco()
            cursor = banco.cursor()

            Destino = request.form['destino']
            Data_ida = request.form['dataida']
            Data_volta = request.form['datavolta']
            Hotel = request.form['hotel']
            Atividades = request.form['atividades']
            Transporte = request.form['transporte']
            Orcamento = request.form['orcamento']
            Acompanhantes = request.form['acompanhantes']
            Moeda = request.form['moeda']

            cursor.execute('''
            INSERT INTO Viagens(
            Destino,Data_ida,Data_volta,Hotel,Atividades,Transporte,Orcamento,Acompanhantes,Moeda)
            VALUES (?,?,?,?,?,?,?,?,?);''',
                           (Destino, Data_ida, Data_volta, Hotel, Atividades, Transporte, Orcamento, Acompanhantes,
                            Moeda))
            banco.commit()
            return redirect('/')


@app.route('/criarcompanhias', methods=['POST', 'GET'])
def CadastrarCompanhias():
        if 'Usuario_Logado' not in session:
            return redirect('/login')
        else:
            banco = ligar_banco()
            cursor = banco.cursor()

            NomeCompanhia = request.form['nomeCompanhia']
            ClasseVoo = request.form['classeVoo']
            HorarioPartida = request.form['horarioPartida']
            PrecoPassagem = request.form['precoPassagem']
            StatusVoo = request.form['statusVoo']

            cursor.execute('''
            INSERT INTO CompanhiasAereas(
            NomeCompanhia,ClasseVoo,HorarioPartida,PrecoPassagem,StatusVoo)
            VALUES (?,?,?,?,?);''',
                           (NomeCompanhia, ClasseVoo, HorarioPartida, PrecoPassagem, StatusVoo))
            banco.commit()
            return redirect('/')


@app.route('/cadastro')
def cadastar():
        if 'Usuario_Logado' not in session:
            return redirect('/login')
        else:
            return render_template('cadastro.html')


@app.route('/cadastrocompanhias')
def cadastarCompanhia():
        if 'Usuario_Logado' not in session:
            return redirect('/login')
        else:
            return render_template('cadastrocompanhia.html')


@app.route('/exibir')
def Exibir():
        if 'Usuario_Logado' not in session:
            return redirect('/login')
        else:
            banco = ligar_banco()
            cursor = banco.cursor()

            cursor.execute('SELECT * FROM Viagens;')
            Viajens = cursor.fetchall()

            return render_template('viajens.html', listaViajens=Viajens)


@app.route('/exibircompanhias')
def ExibirCompanhia():
        if 'Usuario_Logado' not in session:
            return redirect('/login')
        else:
            banco = ligar_banco()
            cursor = banco.cursor()

            cursor.execute('SELECT * FROM CompanhiasAereas;')
            Companhias = cursor.fetchall()

            return render_template('companhias.html', listaCompanhias=Companhias)


@app.route('/excluir/<id>', methods=['GET', 'DELETE'])
def Deletar(id):
        if 'Usuario_Logado' not in session:
            return redirect('/login')
        else:
            banco = ligar_banco()
            cursor = banco.cursor()

            cursor.execute('DELETE FROM Viagens WHERE id=?;', (id,))
            banco.commit()
            return redirect('/exibir')


@app.route('/excluircompanhia/<id>', methods=['GET', 'DELETE'])
def DeletarCompanhia(id):
        if 'Usuario_Logado' not in session:
            return redirect('/login')
        else:
            banco = ligar_banco()
            cursor = banco.cursor()

            cursor.execute('DELETE FROM CompanhiasAereas WHERE id=?;', (id,))
            banco.commit()
            return redirect('/exibircompanhias')


@app.route('/editarcompanhia/<id>', methods=['GET'])
def EditarComp(id):
        if 'Usuario_Logado' not in session:
            return redirect('/login')
        else:
            banco = ligar_banco()
            cursor = banco.cursor()

            cursor.execute('SELECT * FROM CompanhiasAereas WHERE id=?;', (id,))
            encontrado = cursor.fetchone()
            return render_template('editarcompanhias.html', Comp=encontrado, Titulo='Editar Companhia Aérea')


@app.route('/editar/<id>', methods=['GET'])
def Editar(id):
        if 'Usuario_Logado' not in session:
            return redirect('/login')
        else:
            banco = ligar_banco()
            cursor = banco.cursor()

            cursor.execute('SELECT * FROM Viagens WHERE id=?;', (id,))
            encontrado = cursor.fetchone()
            return render_template('editar.html', Viagem=encontrado, Titulo='Editar Viagem')


@app.route('/alterar', methods=['PUT', 'POST'])
def Alterar():
    id = request.form['ide']
    Destino = request.form['destino']
    Data_ida = request.form['dataida']
    Data_volta = request.form['datavolta']
    Hotel = request.form['hotel']
    Atividades = request.form['atividades']
    Transporte = request.form['transporte']
    Orcamento = request.form['orcamento']
    Acompanhantes = request.form['acompanhantes']
    Moeda = request.form['moeda']

    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute('UPDATE Viagens SET Destino=?, Data_ida=?,'
                   'Data_volta=?,Hotel=?,Atividades=?,Transporte=?,Orcamento=?,'
                   'Acompanhantes=?,Moeda=? WHERE id=?;',
                   (Destino, Data_ida, Data_volta, Hotel, Atividades, Transporte, Orcamento, Acompanhantes, Moeda, id))
    banco.commit()
    return redirect('/exibir')


@app.route('/alterarcompanhia', methods=['PUT', 'POST'])
def AlterarComp():
    id = request.form['ide']
    NomeCompanhia = request.form['nomeCompanhia']
    ClasseVoo = request.form['classeVoo']
    HorarioPartida = request.form['horarioPartida']
    PrecoPassagem = request.form['precoPassagem']
    StatusVoo = request.form['statusVoo']

    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute('UPDATE CompanhiasAereas SET NomeCompanhia=?, ClasseVoo=?,'
                   'HorarioPartida=?,PrecoPassagem=?,StatusVoo=? WHERE id=?;',
                   (NomeCompanhia, ClasseVoo, HorarioPartida, PrecoPassagem, StatusVoo, id))
    banco.commit()
    return redirect('/exibircompanhias')


@app.route('/login')
def Login():
    return render_template('Login.html', Titulo='Faça seu Login')


@app.route('/autenticar', methods=['POST'])
def Autenticar():
    Usuario = request.form['usuario']
    Senha = request.form['senha']
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute('SELECT Login, Senha FROM Usuarios;')
    UsuariosBanco = cursor.fetchall()

    for USuarioIndBanco in UsuariosBanco:
        if USuarioIndBanco[0] == Usuario:
            if USuarioIndBanco[1] == Senha:
                session['Usuario_Logado'] = request.form[
                    'usuario']  # session usa os cookies do navegador para armazenar o usuario
                flash('Usuario Logado')  # flash (mensagem rapida que só aparece uma vez)
                return redirect('/')
            else:
                flash('Usuario ou senha incorretos')
                return redirect('/login')
    flash('Usuario ou senha incorretos')
    return redirect('/login')


@app.route('/deslogar')
def Deslogar():
    session.clear()
    return redirect('login')


if __name__ == '__main__':
    app.run()
