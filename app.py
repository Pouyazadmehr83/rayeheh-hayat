from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysupersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
db = SQLAlchemy(app)

# مدل محصول
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50), nullable=True)
    scent = db.Column(db.String(100), nullable=True)
    weight = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

# مدل کاربر ادمین (بدون هش؛ رمز به صورت ساده)
class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()
    # اگر ادمین وجود ندارد، بساز (رمز ساده: admin123)
    if not AdminUser.query.filter_by(username='admin').first():
        admin_user = AdminUser(username='admin', password='admin123')
        db.session.add(admin_user)
        db.session.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    from random import sample
    products = Product.query.all()
    if len(products) > 3:
        featured_products = sample(products, 3)
    else:
        featured_products = products
    return render_template('index.html', featured_products=featured_products)


@app.route('/products')
def products():
    filter_cat = request.args.get('cat', 'all')
    all_products = Product.query.all()
    if filter_cat != 'all':
        all_products = Product.query.filter_by(category=filter_cat).all()
    return render_template('products.html', products=all_products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

categories = {
    "عطر": [],
    "پرفیوم": ["پرفیوم", "ادو پرفیوم", "ادو تویلت", "پرفیوم اکسترا"],
    "ضد تعریق": ["اسپری", "رولی"],
    "خوشبو کننده بدن": [],
    "خوشبو کننده محیط": ["مایع", "اسپری"],
    "شیشه پاک کن": []
}

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        subcategory = request.form.get('subcategory', '')
        scent = request.form.get('scent', '')
        weight = request.form.get('weight', '')
        description = request.form.get('description')
        file = request.files.get('image_file')
        image_url = ''

        if not name or not category or not description or not file:
            flash("لطفاً تمام فیلدها (از جمله تصویر) را پر کنید!", "danger")
            return redirect(url_for('admin_dashboard'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = os.path.join('uploads', filename)
        else:
            flash("فرمت فایل نامعتبر است!", "danger")
            return redirect(url_for('admin_dashboard'))

        try:
            new_product = Product(name=name, category=category, subcategory=subcategory,
                                  scent=scent, weight=weight, description=description,
                                  image_url=image_url)
            db.session.add(new_product)
            db.session.commit()
            flash("محصول با موفقیت اضافه شد!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"خطا در افزودن محصول: {str(e)}", "danger")

        return redirect(url_for('admin_dashboard'))

    all_products = Product.query.all()
    return render_template('admin.html', products=all_products, categories=categories)

@app.route('/admin/delete/<int:product_id>')
def delete_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    p = Product.query.get_or_404(product_id)
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(p.image_url))
    if os.path.exists(img_path):
        os.remove(img_path)
    db.session.delete(p)
    db.session.commit()
    flash("محصول حذف شد!", "warning")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    p = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        p.name = request.form.get('name')
        p.category = request.form.get('category')
        p.subcategory = request.form.get('subcategory', '')
        p.scent = request.form.get('scent', '')
        p.weight = request.form.get('weight', '')
        p.description = request.form.get('description', p.description)

        file = request.files.get('image_file')
        if file and allowed_file(file.filename):
            old_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(p.image_url))
            if os.path.exists(old_path):
                os.remove(old_path)

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            p.image_url = os.path.join('uploads', filename)

        db.session.commit()
        flash("محصول با موفقیت ویرایش شد!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_product.html', product=p, categories=categories)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin_user = AdminUser.query.filter_by(username=username).first()
        if admin_user and admin_user.password == password:
            session['admin_logged_in'] = True
            flash("ورود موفقیت‌آمیز!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("نام کاربری یا رمز عبور اشتباه است!", "danger")
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("از حساب ادمین خارج شدید!", "info")
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
