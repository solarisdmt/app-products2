from flask import request
from flask.views import MethodView
from product_app.module_product.model.product import Product
from product_app import app, db
import json
from product_app.rest_api.helper.request import sendResJson

class ProductApi(MethodView):
    def get(self, id=None):
        products=Product.query.all()
        if id:
            product=Product.query.get(id)
            res=productToJson(product)
        else:
            res=[]
            for product in products:
                res.append(productToJson(product))
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
        
        #Validaciones de precio
        if not 'price' in request.form:
            return sendResJson(None, 'Sin parametro precio', 403)
        
        try:
            price=float(request.form['price'])
        except ValueError:
            return sendResJson(None, 'Precio no valido', 403)
        
        #Validaciones de category_id
        if not 'category_id' in request.form:
            return sendResJson(None, 'Sin parametro category_id', 403)
        
        try:
            price=float(request.form['category_id'])
        except ValueError:
            return sendResJson(None, 'Categoria no valida', 403)
        
        p=Product(request.form.get('name'), request.form.get('price'), request.form.get('category_id'))
        db.session.add(p)
        db.session.commit()
        
        return sendResJson(productToJson(p), None, 200)
    
    def put(self, id):
        p=Product.query.get(id)
        if not p:
            return sendResJson(None, 'Producto no existe', 403)
        
        if not request.form:
            return sendResJson(None, 'Sin parametros', 403)
        #Validaciones de nombre
        if not 'name' in request.form:
            return sendResJson(None, 'Sin parametro nombre', 403)
        
        if len(request.form['name']) < 1:
            return sendResJson(None, 'Nombre no valido', 403)
        
        #Validaciones de precio
        if not 'price' in request.form:
            return sendResJson(None, 'Sin parametro precio', 403)
        
        try:
            price=float(request.form['price'])
        except ValueError:
            return sendResJson(None, 'Precio no valido', 403)
        
        #Validaciones de category_id
        if not 'category_id' in request.form:
            return sendResJson(None, 'Sin parametro category_id', 403)
        
        try:
            price=float(request.form['category_id'])
        except ValueError:
            return sendResJson(None, 'Categoria no valida', 403)
        
        p.name=request.form.get('name')
        p.price=request.form.get('price')
        p.category_id=request.form.get('category_id')
        db.session.add(p)
        db.session.commit()
        
        return sendResJson(productToJson(p), None, 200)
    
    def delete(self, id):
        product=Product.query.get(id)
        if not product:
            return sendResJson(None, 'Producto no existe', 403)
        db.session.delete(product)
        db.session.commit()
        return sendResJson('Producto eliminado', None, 200)

def productToJson(product: Product):
    return {'id': product.id, 
            'name': product.name, 
            'price': product.price,
            'category_id': product.category_id, 
            'category': product.category.name}
    
product_view=ProductApi.as_view('product_view')
app.add_url_rule('/api/products/', view_func=product_view, methods=['GET','POST'])
app.add_url_rule('/api/products/<id>', view_func=product_view, methods=['GET','POST','PUT','DELETE'])
