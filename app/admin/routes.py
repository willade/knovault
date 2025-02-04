from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.models import User, Lesson
from app import db
import plotly.express as px
import pandas as pd

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

@admin.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully')
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/delete_lesson/<int:lesson_id>', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    # Ensure only admins can access this route
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('main.home'))
    
    # Retrieve the lesson and delete it if it exists
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    flash('Lesson deleted successfully.')
    return redirect(url_for('admin.admin_dashboard'))  # Redirect to admin dashboard or another appropriate page

@admin.route('/user_analysis')
@login_required
def user_analysis():
    if current_user.role != 'admin':
        flash('Access denied: Admins only.')
        return redirect(url_for('main.home'))
    
    # Query database for user lesson counts
    user_lesson_counts = db.session.query(
        User.username, db.func.count(Lesson.id).label('lesson_count')
    ).join(Lesson, User.id == Lesson.user_id).group_by(User.username).all()

    # Prepare data for Plotly
    df = pd.DataFrame(user_lesson_counts, columns=['username', 'lesson_count'])
    user_chart = px.bar(
        df, 
        x='lesson_count', 
        y='username', 
        orientation='h',
        title='Lessons per User',
        labels={'lesson_count': 'Number of Lessons', 'username': 'User'}
    ).to_html(full_html=False)

    return render_template('admin_user_analysis.html', user_chart=user_chart)