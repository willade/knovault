from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.models import User, Lesson
from app import db

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied: Admins only.')
        return redirect(url_for('main.home'))
    users = User.query.all()
    lessons = Lesson.query.all()
    return render_template('admin.html', users=users, lessons=lessons)
