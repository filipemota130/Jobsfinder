from flask import render_template, request, redirect, url_for, flash
from app import app, db
from werkzeug.security import generate_password_hash

from app.models.user import User
from app.models.job import Job
from app.models.forms import LoginForm, CadastroForm, CadastroJobForm

current_user = None;
def changeUser(changedUser):
    global current_user
    current_user = changedUser

@app.route('/', defaults={'id': None})
@app.route('/index')
@app.route('/home/<int:id>')
def index(id):
    print(current_user)
    jobs = Job.query.all()
    return render_template('index.html', id=current_user, jobs = jobs)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(form.name.data, form.nick_name.data,
                    form.password.data, form.email.data, form.contact.data, form.birth_date.data, form.desc.data)
            confirmation = User.query.filter_by(email= form.email.data).first()
            if confirmation == None :
                db.session.add(new_user)
                db.session.commit()
                changeUser(new_user.id)
                return redirect(url_for('index',id = current_user))
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
                changeUser(instance.id)
                return redirect(url_for('index',id = current_user))
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
    return 'Tela dos jobs'

@app.route('/cadastroJob', methods=['GET', 'POST'])
def cadastroJobs():
    form = CadastroJobForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_job = Job(form.name.data, form.category.data, form.value.data, form.description.data, form.others.data, current_user)
            db.session.add(new_job)
            db.session.commit()
            return redirect(url_for('index',id = current_user))
        else:
            flash("Erro ao cadastrar serviço")
            print(form.name.errors)
            print(form.category.errors)
            print(form.value.errors)
            print(form.description.errors)
            print(form.others.errors)
    return render_template('cadastroJobs.html', form = form)

@app.route('/delete/<int:id_job>')
def delete(id_job):
    query = Job.query.filter_by(id=id_job).first()
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for('index',id = current_user))

@app.route('/logout')
def logout():
    flash("Sessão encerrada!")
    db.session.expire_all()
    changeUser(None)
    return redirect(url_for('index'))