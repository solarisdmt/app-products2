from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, get_flashed_messages
from product_app.module_category.model.category import Category
from product_app import db
from product_app.module_category.model.category import CategoryForm
from flask_login import login_required
from product_app import rol_admin_need

category=Blueprint('category', __name__)

@category.before_request
@login_required 
@rol_admin_need
def contructor():
    pass
    
@category.route('/category')
@category.route('/category/<int:page>')
def index(page=1):
    return render_template('category/index.html', categories=Category.query.paginate(page=page,per_page=5))

@category.route('/category-show/<int:id>')
def show(id):
    category=Category.query.get_or_404(id)
    return render_template('category/show.html', category=category)

@category.route('/category-delete/<int:id>')
def delete(id):
    category=Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Categoria eliminada con exito')
    return redirect(url_for('category.index'))

@category.route('/category-create', methods=('GET','POST'))
def create():
    form=CategoryForm(meta={'csrf':False})
    if form.validate_on_submit():
        p=Category(request.form.get('name'), request.form.get('price'))
        db.session.add(p)
        db.session.commit()
        flash('Categoria ingresado con exito')
        return redirect(url_for('category.create'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('category/create.html', form=form)

@category.route('/category-update/<int:id>', methods=['GET','POST'])
def update(id):
    category=Category.query.get_or_404(id)
    form=CategoryForm(meta={'csrf':False})
    
    print(category.products) #.first()
    
    if request.method == 'GET':
        form.name.data=category.name
    
    if form.validate_on_submit():
        #Actualizar el categoryo
        category.name=form.name.data
        
        db.session.add(category)
        db.session.commit()
        flash('Categoria ctualizado con exito')
        return redirect(url_for('category.update', id=category.id))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('category/update.html', category=category, form=form)

