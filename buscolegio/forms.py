from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from buscolegio.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email *', validators=[DataRequired(), Email()])
    username = StringField('Nombre *', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Contraseña *', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña *', validators=[DataRequired(), EqualTo('password')])
    image_file = FileField('Imagen De Perfil *', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    role = SelectField(u'Soy:', choices=[('user', 'Padre / Madre'), ('inst', 'Institución')])
    submit = SubmitField('Registrar')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Esa cuenta de email ya ha sido utilizada, por favor seleccionar otra')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usario ya ha sido utilizado, por favor seleccionar otro')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuerdame')
    submit = SubmitField('Ingresar')

class UpdateInstituteForm(FlaskForm):
    email = StringField('Email *', validators=[DataRequired(), Email()])
    name = StringField('Nombre Institución *', validators=[DataRequired(), Length(min=2, max=20)])
    cover_picture = FileField('Imagen De Portada', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    url = StringField('Página Web')
    address = StringField('Dirección *', validators=[DataRequired()])
    phone =  IntegerField('Teléfono')
    est = DateTimeField('Fundado', format='%m/%d/%y')
    description = TextAreaField('Descripción')
    state = SelectField('Departamento', choices=[('Artigas', 'Artigas'), ('Canelones', 'Canelones'), ('Cerro Largo', 'Cerro Largo'),
                                                ('Colonia', 'Colonia'), ('Durazno', 'Durazno'), ('Flores', 'Flores'), ('Florida', 'Florida'),
                                                ('Lavalleja', 'Lavalleja'), ('Maldonado', 'Maldonado'), ('Montevideo', 'Montevideo'),
                                                ('Paysandú', 'Paysandú'), ('Río Negro', 'Río Negro'), ('Rivera', 'Rivera'),
                                                ('Rocha', 'Rocha'), ('Salto', 'Salto'), ('San José', 'San José'), ('Soriano', 'Soriano'),
                                                ('Tacuarembó', 'Tacuarembó'), ('Treinta y Tres', 'Treinta y Tres')])
    loc = StringField('Localidad') # , validators=[DataRequired()]
    teachers = IntegerField('Cantidad De Profesores')
    classrooms = IntegerField('Cantidad de Aulas')
    rel_conf = StringField('Confesión Religiosa')
    level = SelectField(u'Nivel', choices=[('Inicial', 'Inicial'), ('Primaria', 'Primaria',), ('Secundaria', 'Secundaria') ])
    enrollment = IntegerField('Matricula')
    fee = IntegerField('Cuota Mensual')
    submit = SubmitField('Enviar')

class UpdateUserForm(FlaskForm):
    email = StringField('Email *', validators=[DataRequired(), Email()])
    username = StringField('Nombre de Usuario *', validators=[DataRequired(), Length(min=2, max=20)])
    image_file = FileField('Imagend de Perfil')
    submit = SubmitField('Enviar')

class SearchForm(FlaskForm):
    search = StringField('Buscar Institución')
    submit = SubmitField('Aceptar')

class CompareForm(FlaskForm):
    submit = SubmitField('Comparar')
