from flask import render_template
from app import app

@app.route('/', defaults ={ 'id' : None})
@app.route('/index')
@app.route('/home/<int:id>')
def index(id):
    return render_template('index.html', id=id)

@app.route('/Cadastro', methods=['GET','POST'])
def cadastro():
    return 'Cadastro page'

@app.route('/Login', methods=['GET','POST'])
def login():
    return 'Login page'

@app.route('/perfil')
def perfil():
        return render_template('index.html')

@app.route('/jobs')
def jobs():
        return 'Jobs page'