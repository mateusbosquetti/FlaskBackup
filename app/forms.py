from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import db, bcrypt, app
from app.models import Contato, PostComentarios, User, Post

import os
from werkzeug.utils import secure_filename


class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(),Email()]) 
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confimar senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')

    def validade_email(self, email):
        if User.query.filter(email=email.data).first():
            return ValidationError('Usuário já cadastradado com esse E-mail!!!')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha
        )
        db.session.add(user)
        db.session.commit()
        return user

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(),Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self):
        contato = Contato(
            nome = self.nome.data,
            email = self.email.data,
            assunto = self.assunto.data,
            mensagem = self.mensagem.data
        )
        db.session.add(contato)
        db.session.commit()

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, 
                                        self.senha.data.encode('utf-8')):
                    return user
            else:
                    raise Exception('Senha Incorreta!!!')
        else:
            raise Exception('Usuario nao encontrado')

class PostForm(FlaskForm):
     mensagem = StringField('Mensagem', validators=[DataRequired()])
     imagem = FileField('Imagem', validators=[DataRequired()])
     btnSubmit = SubmitField('Enviar')

     def save(self, user_id):
        imagem = self.imagem.data
        nome_seguro = secure_filename(imagem.filename)
        post = Post (
             mensagem=self.mensagem.data,
             user_id=user_id,
             imagem=nome_seguro
        )
        caminho = os.path.join(
             os.path.abspath(os.path.dirname(__file__)),
             app.config['UPLOAD_FILES'],
             'post',
             nome_seguro
        )
        imagem.save(caminho)
        db.session.add(post)
        db.session.commit()

class PostComentarioForm(FlaskForm):
     comentario = StringField('Comentario', validators=[DataRequired()])
     btnSubmit = SubmitField('Enviar')

     def save(self, user_id, post_id):
        comentario = PostComentarios (
             comentario=self.comentario.data,
             user_id= user_id,
             post_id = post_id
        )

        db.session.add(comentario)
        db.session.commit()