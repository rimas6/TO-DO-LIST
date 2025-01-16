from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime



app = Flask(__name__)



# إعداد قاعدة البيانات (SQLite)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # اسم ملف قاعدة البيانات

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



# تعريف نموذج المهمة

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)  # رقم المهمة (معرف فريد)

    content = db.Column(db.String(200), nullable=False)  # نص المهمة

    due_date = db.Column(db.DateTime, nullable=True)  # تاريخ الاستحقاق

    completed = db.Column(db.Boolean, default=False)  # حالة المهمة (تم/لم يتم)



# إنشاء قاعدة البيانات إذا لم تكن موجودة

with app.app_context():

    db.create_all()



# الصفحة الرئيسية - عرض المهام

@app.route('/')

def home():

    tasks = Task.query.order_by(Task.due_date).all()  # جلب جميع المهام مرتبة حسب تاريخ الاستحقاق

    return render_template('index.html', tasks=tasks)



# إضافة مهمة جديدة

@app.route('/add', methods=['POST'])

def add_task():

    content = request.form.get('content')  # جلب نص المهمة

    due_date = request.form.get('due_date')  # جلب تاريخ الاستحقاق

    

    if content:  # التحقق من أن النص غير فارغ

        new_task = Task(

            content=content,

            due_date=datetime.strptime(due_date, '%Y-%m-%d') if due_date else None

        )

        db.session.add(new_task)  # إضافة المهمة إلى قاعدة البيانات

        db.session.commit()  # حفظ التغييرات

        return redirect(url_for('home'))

    else:

        return "Task content is required!", 400  # إذا كان النص فارغًا



# تغيير حالة المهمة (تم/لم يتم)

@app.route('/complete/<int:task_id>')

def complete_task(task_id):

    task = Task.query.get_or_404(task_id)

    task.completed = not task.completed  # عكس حالة المهمة

    db.session.commit()  # حفظ التغييرات

    return redirect(url_for('home'))



# حذف مهمة

@app.route('/delete/<int:task_id>')

def delete_task(task_id):

    task = Task.query.get_or_404(task_id)

    db.session.delete(task)  # حذف المهمة

    db.session.commit()  # حفظ التغييرات

    return redirect(url_for('home'))



if __name__ == '__main__':

    app.run(debug=True)