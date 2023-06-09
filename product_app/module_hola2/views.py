from flask import Blueprint

hola2=Blueprint('hola2', __name__)

@hola2.route('/')
@hola2.route('/hola2')
def hola2_method():
    return 'Hola mundo 2 blueprint'