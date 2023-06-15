from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

from functools import wraps # Para maneho de decoradores para sesiones

app=Flask(__name__)

app.config.from_object('configuration.DevelopmentConfig')
db=SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='fauth.login'

from product_app.module_auth.views_auth import logout

def rol_admin_need(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if current_user.rol.value != 'admin':
            logout()
            return redirect(url_for('fauth.login'))
            #login_manager.unauthorized()
            #return 'Tu debes ser un admin',403
            #print('Calling decorated function ' + str(current_user.rol.value))
        return f(*args, **kwds)
    return wrapper

#importar las vistas
from product_app.module_product.views_product import product
from product_app.module_category.views_category import category
#from product_app.module_auth.views_auth import auth
from product_app.module_auth.fauth.views_auth import fauth

app.register_blueprint(product)
app.register_blueprint(category)
#app.register_blueprint(auth)
app.register_blueprint(fauth)

with app.app_context():
    db.create_all()
   
 
def reverse_filter(s):
     return s[::-1]

def mydouble_filter(n:int):
    return n*2

app.jinja_env.filters['mydouble'] = mydouble_filter
app.jinja_env.filters['reverse_filter'] = reverse_filter