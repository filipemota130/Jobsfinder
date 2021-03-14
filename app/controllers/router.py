from flask import render_template, request, redirect, url_for, flash
from app import app, db, login_manager
from flask_login import current_user, login_user, logout_user

from app.models.user import User
from app.models.job import Job
from app.models.forms import LoginForm, CadastroForm, CadastroJobForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
@app.route('/presentation')
def presentation():
    return render_template('presentation.html')

@app.route('/', defaults={'id': None})
@app.route('/index/<id>')
@app.route('/home/<id>')
def index(id):
    if not current_user.is_authenticated:
        return redirect(url_for('presentation'))
    print(current_user)
    jobs = Job.query.all()
    return render_template('index.html', id= current_user.id, jobs = jobs)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('index',id = current_user))
    form = CadastroForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(form.name.data, form.nick_name.data, form.email.data, form.contact.data, form.birth_date.data, form.desc.data)
            new_user.set_senha(form.password.data)
            confirmation = User.query.filter_by(email= form.email.data).first()
            if confirmation == None :
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('index', id = current_user))
            else : 
                flash("usuário já existente")
                return redirect(url_for('cadastro'))
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
    if current_user.is_authenticated:
        return redirect(url_for('index',id = current_user))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash("Login confirmado!")
            instance = User.query.filter_by(email= form.email.data).first()
            if instance == None or instance.check_senha(form.password.data) == False:
                flash("usuário inexistente")
                return redirect(url_for('login'))
            if (form.remember_me.data):
                login_user(instance, remember=True)
                return redirect(url_for('index', id=current_user))

            login_user(instance)
            return redirect(url_for('index', id=current_user))
        else:
            print(form.email.errors)
            print(form.password.errors)

    return render_template('login.html', form=form)


@app.route('/meuperfil')
def meuperfil():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user= User.query.filter_by(id=current_user.id).first()
    return render_template('perfil.html', id=current_user.id, user= user)

@app.route('/perfil/<int:id>')
def perfil(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user= User.query.filter_by(id=id).first()
    return render_template('perfil.html', user=user)

@app.route('/cadastroJob/<int:id>', methods=['GET', 'POST'])
def cadastroJobs(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = CadastroJobForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(id=current_user.id).first()
            new_job = Job(form.name.data, form.category.data, form.value.data, form.description.data, form.others.data, current_user.id, user.nick_name)
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
    return render_template('cadastroJobs.html', form = form, id=id)

@app.route('/delete/<int:id_job>')
def delete(id_job):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    query = Job.query.filter_by(id=id_job).first()
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for('index',id = current_user))

@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    flash("Sessão encerrada!")
    logout_user();
    return redirect(url_for('presentation'))