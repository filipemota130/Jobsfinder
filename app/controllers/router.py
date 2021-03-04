from flask import render_template
from app import app

from app.models.forms import LoginForm, CadastroForm

@app.route('/', defaults ={ 'id' : None})
@app.route('/index')
@app.route('/home/<int:id>')
def index(id):
    return render_template('index.html', id=id)

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        print(form.email.data)
        print(form.password.data)
        print(form.name.data)
        print(form.nickname.data)
        print(form.contact.data)
        print(form.birth_date.data)
        print(form.adress.data)
        print(form.compAdress.data)
        print(form.state.data)
        print(form.city.data)
    else:
        print(form.email.errors)
        print(form.password.errors)
        print(form.name.errors)
        print(form.nickname.errors)
        print(form.contact.errors)
        print(form.birth_date.errors)
        print(form.adress.errors)
        print(form.compAdress.errors)
        print(form.state.errors)
        print(form.city.errors)
    return render_template("cadastro.html", form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)
        print(form.remember_me.data)
    else:
        print(form.username.errors)
        print(form.password.errors)
    
    return render_template('login.html', form=form)

@app.route('/perfil')
def perfil():
        return render_template('index.html')

@app.route('/jobs')
def jobs():
        return 'Jobs page'