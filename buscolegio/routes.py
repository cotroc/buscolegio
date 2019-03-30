import os
import secrets
from flask import render_template, url_for, flash, redirect, request, session, abort
from buscolegio import app, db, bcrypt
from buscolegio.forms import RegistrationForm, LoginForm, UpdateUserForm, UpdateInstituteForm, SearchForm, CompareForm
from buscolegio.models import Instituto, Extra, User
from flask_login import login_user, current_user, logout_user, login_required

""" 
Home page.
"""
@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html') 

""" 
About page.
"""
@app.route("/about")
def about():
    return render_template('about.html', title='About')

""" 
User register.
"""
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
        if form.image_file.data != None:
            user.image_file = save_picture(form.image_file.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Usuario {form.username.data} creado! Ya puedes ingresar.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registro', form=form)


""" 
User login
"""
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=(request.args.get('next'))
            flash('Has ingresado al sistema!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('user'))
        else:
            flash('Login Incorrecto. Por favor, comprueba el usuario y la contraseña', 'danger')
    return render_template('login.html', title='Login', form=form)


""" 
User Logout
"""
@app.route("/logout")
def logout():
    logout_user()

    return redirect(url_for('home'))


""" 
Save picture files to the server
"""
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


""" 
User home page.
"""
@app.route("/user", methods=['GET', 'POST'])
@login_required
def user():
    form = UpdateUserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        if form.image_file.data != None:
            current_user.image_file = save_picture(form.image_file.data)
        db.session.commit()
        flash('Linformación de usuario ha sido acutualizada con éxito', 'success')
        return redirect(url_for('user'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.image_file.data = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user.html', title='Usuario', form=form)

"""
User search page.
"""
@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    if current_user.role != 'user':
        abort(403)
    form = SearchForm()
    c_form = CompareForm()
    institutos = []
    profile_pic = url_for('static', filename='profile_pics/' + current_user.image_file)
    if form.validate_on_submit():
        institutos = Instituto.query.filter(Instituto.name.like('%{}%'.format(form.search.data))).all()
        print(len(institutos))
        if request.form.getlist('selected'):
            session['selected'] = request.form.getlist('selected')
            print(session['selected'])
            return redirect(url_for('compare'))
    flash(f'Consejo: Si realizas una busqueda con el campo vacío se listarán todos los Colegios', 'info')            
    return render_template('search.html', title='Usuario', profile_pic=profile_pic, form=form, c_form=c_form, institutos=institutos)

""" 
User update page
"""
@app.route("/user/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
def user_update(user_id):
    form = UpdateUserForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        if form.image_file.data != None:
            current_user.image_file = save_picture(form.image_file.data)
        db.session.commit()
        flash('Linformación de usuario ha sido acutualizada con éxito', 'success')
        return redirect(url_for('user'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.image_file.data = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user_update.html', title='Opciones de Usuario', form=form)


""" 
Colegio home page.
"""
@app.route("/colegio", methods=['GET', 'POST'])
@login_required
def colegio():
    if current_user.role != 'inst':
        abort(403)
    return render_template('colegio.html')

""" 
Colegio create page
"""
@app.route("/colegio/create", methods=['GET', 'POST'])
@login_required
def colegio_create():
    if current_user.role != 'inst':
        abort(403)
    form = UpdateInstituteForm()
    if form.validate_on_submit():
        instituto = Instituto( name=form.name.data, email=form.email.data, url=form.url.data, 
                            address=form.address.data, phone=form.phone.data, est=form.est.data, 
                            description=form.description.data, state=form.state.data, loc=form.loc.data, 
                            teachers=form.teachers.data, classrooms=form.classrooms.data, rel_conf=form.rel_conf.data, 
                            level=form.level.data, enrollment=form.enrollment.data, fee=form.fee.data, 
                            responsable=current_user)
        if form.cover_picture.data != None:
            instituto.cover_picture = save_picture(form.cover_picture.data) 
        db.session.add(instituto)
        db.session.commit()
        flash('Instituto {} creado con exito'.format(instituto.name), 'success')
        return redirect(url_for('user'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('colegio_update.html', title='Datos del Instituto', form=form)

""" 
Colegio update page
"""
@app.route("/colegio/update", methods=['GET', 'POST'])
@login_required
def colegio_update():
    if current_user.role != 'inst':
        abort(403)
    form = UpdateInstituteForm()
    if form.validate_on_submit():
        instituto = Instituto.query.filter_by(responsable=current_user).first()
        instituto.name = form.name.data
        instituto.email = form.email.data
        instituto.url = form.url.data
        instituto.address = form.address.data
        instituto.phone = form.phone.data
        instituto.est = form.est.data
        instituto.description = form.description.data
        instituto.state = form.state.data
        instituto.loc = form.loc.data
        instituto.teachers = form.teachers.data
        instituto.classrooms = form.classrooms.data
        instituto.rel_conf = form.rel_conf.data
        instituto.level = form.level.data
        instituto.enrollment = form.enrollment.data
        instituto.fee = form.fee.data
        responsable = current_user
        if form.cover_picture.data != None:
            cover_picture = save_picture(form.cover_picture.data)
        db.session.commit()
        flash('Instituto actualizado con exito', 'success')
        return redirect(url_for('colegio_update'))
    elif request.method == 'GET':
        instituto = Instituto.query.filter_by(responsable=current_user).first() # instituto/actualizar
        form.name.data = instituto.name
        form.email.data = instituto.email
        form.cover_picture.data = url_for('static', filename='profile_pics/' + instituto.cover_picture)
        form.url.data = instituto.url
        form.address.data = instituto.address
        form.phone.data = instituto.phone
        form.est.data = instituto.est
        form.description.data = instituto.description
        form.state.data = instituto.state
        form.loc.data = instituto.loc
        form.teachers.data = instituto.teachers
        form.classrooms.data = instituto.classrooms
        form.rel_conf.data = instituto.rel_conf
        form.level.data = instituto.level
        form.enrollment.data = instituto.enrollment
        form.fee.data = instituto.fee
    return render_template('colegio_update.html', title='Datos del Instituto', form=form)

"""
Colegio extras
"""
@app.route("/instituto/extras")
@login_required
def extras():
    if current_user.role != 'inst':
        abort(403)
    return render_template('extras.html')

"""
Colegio details page.
"""
@app.route("/instituto/details/<int:instituto_id>")
@login_required
def details(instituto_id):
    instituto = Instituto.query.get_or_404(instituto_id)
    return render_template('details.html', title=instituto.name, instituto=instituto)

"""
Colegio comparison page.
"""
@app.route("/compare", methods=['GET', 'POST'])
@login_required
def compare():
    if current_user.role != 'user':
        abort(403)
    form = SearchForm()
    list_id = session['selected']
    institutos = []
    if form.validate_on_submit():
        print('POST')
    elif request.method == 'GET':
        for item in list_id:
            institutos.append(Instituto.query.get(item))
    return render_template('compare.html', form=form, institutos=institutos) # 

"""
403
"""
@app.errorhandler(403)
def forbiden_access(e):
    message = "403 Denegado: No tienes permisos suficientes para acceder a este recurso."
    # note that we set the 404 status explicitly
    return render_template('403.html', message=message), 403
