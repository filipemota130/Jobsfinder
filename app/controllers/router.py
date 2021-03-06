from flask import render_template, request, redirect, url_for, flash
from app import app, db
from werkzeug.security import generate_password_hash

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
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method = 'sha256')
            password = hashed_password
            new_user = User(form.name.data, form.nick_name.data,
                    password, form.email.data, form.contact.data, form.birth_date.data, form.desc.data)
            confirmation = User.query.filter_by(email= form.email.data).first()
            if confirmation == None :
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('index',id = new_user.id))
            else : 
                flash("usuário já existente")
        else:
            print(form.email.errors)
            print(form.password.errors)
            print(form.name.errors)
            print(form.nick_name.errors)
            print(form.contact.errors)
            print(form.birth_date.errors)

    return render_template("cadastro.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash("Login confirmado!")
            instance = User.query.filter_by(email= form.email.data, password =form.password.data).first()
            if instance:
                db.session.add(instance)
                db.session.commit()
                return redirect(url_for('index',id = instance.id))
            else :
                flash("usuário inexistente")
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


@app.route('/logout')
def logout():
    flash("Sessão encerrada!")
    db.session.expire()
    return redirect(url_for('index'))