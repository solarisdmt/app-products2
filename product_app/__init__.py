from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config.from_object('configuration.DevelopmentConfig')
db=SQLAlchemy(app)

#importar las vistas
from product_app.module_product.views_product import product
from product_app.module_category.views_category import category
app.register_blueprint(product)
app.register_blueprint(category)

with app.app_context():
    db.create_all()
    
def reverse_filter(s):
     return s[::-1]

def mydouble_filter(n:int):
    return n*2

app.jinja_env.filters['mydouble'] = mydouble_filter
app.jinja_env.filters['reverse_filter'] = reverse_filter