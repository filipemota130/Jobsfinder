from flask import render_template, request, redirect, url_for
from app import app, db

from app.models.user import User
from app.models.forms import LoginForm, CadastroForm


@app.route('/', defaults={'id': None})
@app.route('/index')
@app.route('/home/<int:id>')
def index(id):
    return render_template('index.html', id=id)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        print(form.email.data)
        print(form.password.data)
        print(form.name.data)
        print(form.nick_name.data)
        print(form.contact.data)
        print(form.birth_date.data)
        # i = User(form.name.data, form.nick_name.data,
        #        form.password.data, form.email.data, form.contact.data, form.birth_date.data, form.desc.data)
    else:
        print(form.email.errors)
        print(form.password.errors)
        print(form.name.errors)
        print(form.nick_name.errors)
        print(form.contact.errors)
        print(form.birth_date.errors)
    return render_template("cadastro.html", form=form)


@app.route('/login', methods=['GET', 'POST'], defaults={'info': None})
def login(info):
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            r = User.query.filter_by(email= form.email.data, password =form.password.data).first()
            if r:
                db.session.add(r)
                db.session.commit()
                return redirect(url_for('index',id = r.id))
            else :
                return("usuário inexistente")
        else:
            print(form.email.errors)
            print(form.password.errors)

    return render_template('login.html', form=form)


@app.route('/perfil')
def perfil():
    return render_template('index.html')


@app.route('/jobs')
def jobs():
    return 'Jobs page'
