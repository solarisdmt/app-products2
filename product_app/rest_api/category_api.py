from flask import request
from flask.views import MethodView
from product_app.module_category.model.category import Category
from product_app import app, db
import json
from product_app.rest_api.helper.request import sendResJson

class CategoryApi(MethodView):
    def get(self, id=None):
        categories=Category.query.all()
        if id:
            category=Category.query.get(id)
            res=categoryToJson(category)
        else:
            res=[]
            for category in categories:
                res.append(categoryToJson(category))
        #return sendResJson(res, None, 200)
        return sendResJson(res,None,200)
    
    def post(self):
        if not request.form:
            return sendResJson(None, 'Sin parametros', 403)
        #Validaciones de nombre
        if not 'name' in request.form:
            return sendResJson(None, 'Sin parametro nombre', 403)
        
        if len(request.form['name']) < 1:
            return sendResJson(None, 'Nombre no valido', 403)
        
       
        p=Category(request.form.get('name'))
        db.session.add(p)
        db.session.commit()
        
        return sendResJson(categoryToJson(p), None, 200)
    
    def put(self, id):
        p=Category.query.get(id)
        if not p:
            return sendResJson(None, 'Categoria no existe', 403)
        
        if not request.form:
            return sendResJson(None, 'Sin parametros', 403)
        #Validaciones de nombre
        if not 'name' in request.form:
            return sendResJson(None, 'Sin parametro nombre', 403)
        
        if len(request.form['name']) < 1:
            return sendResJson(None, 'Nombre no valido', 403)           
       
        p.name=request.form.get('name')
        db.session.add(p)
        db.session.commit()
        
        return sendResJson(categoryToJson(p), None, 200)
    
    def delete(self, id):
        category=Category.query.get(id)
        if not category:
            return sendResJson(None, 'Categoria no existe', 403)
        db.session.delete(category)
        db.session.commit()
        return sendResJson('Categoria eliminada', None, 200)

def categoryToJson(category: Category):
    return {'id': category.id, 
            'name': category.name,
            }
    
category_view=CategoryApi.as_view('category_view')
app.add_url_rule('/api/categories/', view_func=category_view, methods=['GET','POST'])
app.add_url_rule('/api/categories/<id>', view_func=category_view, methods=['GET','POST','PUT','DELETE'])
