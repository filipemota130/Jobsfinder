from flask import render_template, request, redirect, url_for, flash, abort
from app import app, db, login_manager
from flask_login import current_user, login_user, logout_user
import string , random
from app.models.user import User
from app.models.job import Job
from app.models.forms import LoginForm, CadastroForm, CadastroJobForm, EditarForm, EditarJobForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/presentation')
def presentation():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('presentation.html')


@app.route('/index/<id>')
@app.route('/home/<id>')
@app.route('/', defaults={ 'id' : None })
def index(id):
    if not current_user.is_authenticated:
        return redirect(url_for('presentation'))
    print(current_user)
    jobs = Job.query.all()
    return render_template('index.html', id=current_user.id, jobs=jobs)


@app.errorhandler(404)
def client_error(error):
    return render_template('error.html', error_cod=404, desc_error='Página não encontrada'), 404


@app.errorhandler(500)
def server_error(error):
    db.session.rollback()
    return render_template('error.html', erro_cod=500, desc_error='Erro no servidor'), 500


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('index', id=current_user))
    form = CadastroForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(form.name.data, form.nick_name.data, form.email.data,
                            form.contact.data, form.birth_date.data, form.desc.data)
            new_user.set_senha(form.password.data)
            confirmation = User.query.filter_by(email=form.email.data).first()
            if confirmation == None:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('index', id=current_user))
            else:
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

@app.route('/editar/<int:id_user>', methods=['GET', 'POST'])
def editar(id_user):
    if not current_user.is_authenticated:
        return redirect(url_for('presentation'))
    form = EditarForm()
    user= User.query.filter_by(id=id_user).first()
    print(user)
    if request.method == 'POST':
        if form.validate_on_submit():
            user.nick_name = form.nick_name.data
            if (form.password.data == ''):
                form.password.data = user.password
            user.set_senha(form.password.data)
            if (form.desc.data == ''):
                form.desc.data = user.desc
            user.desc = form.desc.data
            user.date= form.birth_date.data
            user.number = form.contact.data
            db.session.commit()
        else:
            return 'erro de validação'
        return redirect(url_for('index', id=current_user))
    return render_template("Editar.html", form=form, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index', id=current_user))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash("Login confirmado!")
            instance = User.query.filter_by(email=form.email.data).first()
            if instance is None or not instance.check_senha(form.password.data):
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
    user = User.query.filter_by(id=current_user.id).first()
    return render_template('perfil.html', id=current_user.id, user=user)


@app.route('/perfil/<int:id>')
def perfil(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.filter_by(id=id).first()
    return render_template('perfil.html', user=user)


@app.route('/cadastroJob/<int:id>', methods=['GET', 'POST'])
def cadastroJobs(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = CadastroJobForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(id=current_user.id).first()
            identifier = randomword(200)
            new_job = Job(form.name.data, form.category.data, form.value.data,
                          form.description.data, form.others.data, current_user.id, user.nick_name, identifier)
            db.session.add(new_job)
            db.session.commit()
            return redirect(url_for('index', id=current_user))
        else:
            flash("Erro ao cadastrar serviço")
            print(form.name.errors)
            print(form.category.errors)
            print(form.value.errors)
            print(form.description.errors)
            print(form.others.errors)
    return render_template('cadastroJobs.html', form=form, id=id)


@app.route('/EditarJob/<int:id>', methods=['GET', 'POST'])
def EditarJobs(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = EditarJobForm()
    job = Job.query.filter_by(id=id).first()
    if job is None:
        return abort(404)
    if request.method == 'POST':
        if form.validate_on_submit():
            job.name= form.name.data
            job.category= form.category.data
            job.valor= form.value.data
            if (form.description.data == ''):
                form.description.data = job.desc
            job.desc= form.description.data
            job.outros = form.others.data
            db.session.commit()
            return redirect(url_for('index', id=current_user))
        else:
            flash("Erro ao cadastrar serviço")
            print(form.name.errors)
            print(form.category.errors)
            print(form.value.errors)
            print(form.description.errors)
            print(form.others.errors)
    return render_template('EditarJobs.html', form=form, id=id, job=job)


@app.route('/delete/<int:id_job>')
def delete(id_job):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    query = Job.query.filter_by(id=id_job).first()
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for('index', id=current_user))


@app.route('/delete_user/<int:id_user>')
def delete_user(id_user): 
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    query = User.query.filter_by(id=id_user).first()
    query2= Job.query.filter_by(id_user=id_user).all()
    for i in query2:
        db.session.delete(query2)
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for('presentation'))


@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    flash("Sessão encerrada!")
    logout_user()
    return redirect(url_for('presentation'))


def randomword(size):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(size))