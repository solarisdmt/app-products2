from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, get_flashed_messages
from product_app.module_product.model.products import PRODUCTS
from product_app.module_product.model.product import Product
from product_app import db
from product_app.module_product.model.product import ProductForm


product=Blueprint('product', __name__)

@product.route('/test')
def test():
    products=Product.query.paginate(page=1,per_page=5).items
    print(products)
    return render_template('product/index.html')
    
@product.route('/product')
@product.route('/product/<int:page>')
def index(page=1):
    return render_template('product/index.html', products=Product.query.paginate(page=page,per_page=5))

@product.route('/product/<int:id>')
def show(id):
    #product=PRODUCTS.get(id)
    product=Product.query.get_or_404(id)
    print(type(product))
    #if not product:
    #    abort(404)
    return render_template('product/show.html', product=product)

@product.route('/product-delete/<int:id>')
def delete(id):
    product=Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado con exito')
    return redirect(url_for('product.index'))

@product.route('/product-create', methods=('GET','POST'))
def create():
    #print(get_flashed_messages())
    form=ProductForm(meta={'csrf':False})
    if form.validate_on_submit():
        p=Product(request.form.get('name'), request.form.get('price'))
        db.session.add(p)
        db.session.commit()
        flash('Producto ingresado con exito')
        return redirect(url_for('product.create'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('product/create.html', form=form)

@product.route('/product-update/<int:id>', methods=['GET','POST'])
def update(id):
    product=Product.query.get_or_404(id)
    form=ProductForm(meta={'csrf':False})
    
    if request.method == 'GET':
        form.name.data=product.name
        form.price.data=product.price
    
    if form.validate_on_submit():
        #Actualizar el producto
        product.name=form.name.data
        product.price=form.price.data
        
        db.session.add(product)
        db.session.commit()
        flash('Producto actualizado con exito')
        return redirect(url_for('product.update', id=product.id))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('product/update.html', product=product, form=form)

@product.route('/filter/<int:id>')
def filter(id):
    product=PRODUCTS.get(id)
    return render_template('product/filter.html', product=product)

@product.app_template_filter('igv')
def igv_filter(product):
    if product['price']:
        return product['price'] * 1.18
    return 'Sin precio'
