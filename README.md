# 🌸 Rayeheh Hayat | رایحه حیات

A **perfume & cologne showcase website** built with [Flask](https://flask.palletsprojects.com/) and **SQLite3** database.  
این وبسایت با فریمورک فلاسک ساخته شده و برای معرفی و مدیریت محصولات عطر و ادکلن طراحی شده است.  
دارای **رابط کاربری کاربرپسند** و **داشبورد مدیریت** برای اضافه/حذف/ویرایش محصولات می‌باشد.  

---

## ✨ Features | ویژگی‌ها

### User Side | سمت کاربر
- 🛍️ مشاهده عطرها و ادکلن‌ها با جزئیات
- 🔍 جستجو و مرور محصولات
- 🎨 رابط کاربری ساده و کاربرپسند

### Admin Side | سمت مدیریت
- ➕ افزودن محصولات جدید
- ✏️ ویرایش اطلاعات محصولات
- ❌ حذف محصولات
- 📊 داشبورد مدیریت

### Technical | فنی
- Backend: **Flask**
- Database: **SQLite3**
- Templates: **HTML + Jinja2**
- Static Files: **CSS / JS**
- Admin Dashboard integrated

---

## 🛠 Installation & Run | نصب و اجرا

### Prerequisites | پیش‌نیازها
- Python 3.8+
- pip
- (Optional) Virtual environment

### Steps | مراحل
```bash
# 1. Clone the repository | کلون کردن ریپو
git clone https://github.com/Pouyazadmehr83/rayeheh-hayat.git
cd rayeheh-hayat

# 2. (Optional) Create virtual environment | محیط مجازی (اختیاری)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# 3. Install dependencies | نصب وابستگی‌ها
pip install -r requirements.txt

# 4. Run the app | اجرای پروژه
flask run
