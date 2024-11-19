from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Lesson
from app.forms import LoginForm, RegistrationForm, ProfileForm
from datetime import datetime
from app.analytics import get_most_common_issues, get_trends_by_phases, generate_issue_trend_chart, generate_phase_insights_chart, generate_tag_usage_chart, generate_project_status_chart, generate_avg_duration_chart, generate_recommendation_wordcloud, generate_completion_trend_chart, generate_lessons_vs_duration_chart
import plotly.express as px

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if form.validate_on_submit():
            print("Form submitted and validated.")   # Debugging statement
            # Check if a user with the same email or username exists
            existing_user = User.query.filter_by(email=form.email.data).first() or User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash("User with this email or username already exists.", "warning")
                print("User with this email or username already exists.")  # Debugging statement
                return redirect(url_for('main.register'))
            
            # Create a new user instance
            user = User(
                full_name=form.full_name.data,
                username=form.username.data,
                email=form.email.data,
                project_role=form.project_role.data,
                terms_accepted=form.terms_accepted.data
                #role='user'
            )
            user.set_password(form.password.data)
            print("Form validated. Preparing to create user.")   #delete later

            # Add to the session and commit
            
            db.session.add(user)
            db.session.commit()
            print("Form validated and creating user.")   #delete later

            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('main.login'))
        else:
            print ('form is not validated')
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile updated!')
        return redirect(url_for('main.profile'))
    
    # Pre-fill the form with current user data
    form.username.data = current_user.username
    form.email.data = current_user.email
    lessons = Lesson.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', user=current_user, lessons=lessons, form=form)

    # if request.method == 'POST':
    #     current_user.username = request.form['username']
    #     current_user.email = request.form['email']
    #     db.session.commit()
    #     flash('Profile updated!')
    # lessons = Lesson.query.filter_by(user_id=current_user.id).all()
    # return render_template('profile.html', user=current_user, lessons=lessons)

@main.route('/')
@login_required
def home():
    lessons = Lesson.query.order_by(Lesson.id.desc()).limit(5).all()
    # Generate charts
    issue_chart = generate_issue_trend_chart()  # If using a bar chart
    phase_chart = generate_phase_insights_chart()
    tag_chart = generate_tag_usage_chart()

    return render_template(
        'home.html',
        lessons=lessons,
        issue_chart=issue_chart,
        phase_chart=phase_chart,
        tag_chart=tag_chart
    )


@main.route('/change_password', methods=['POST'])
@login_required
def change_password():
    new_password = request.form['new_password']
    if new_password:
     current_user.set_password(new_password)
    db.session.commit()
    flash('Password updated successfully.')
    return redirect(url_for('main.profile'))

@main.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_lesson():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']
        project_start_date = request.form.get('project_start_date')
        project_end_date = request.form.get('project_end_date')
        project_status = request.form.get('project_status')
        project_phase = request.form['project_phase']
        issue_type = request.form['issue_type']
        solution = request.form['solution']
        recommendation = request.form['recommendation']
        tags = request.form['tags']

        # Convert dates from string to datetime if provided
        if project_start_date:
            project_start_date = datetime.strptime(project_start_date, '%Y-%m-%dT%H:%M')
        else:
            project_start_date = None  # Ensure None if not provided

        if project_end_date:
            project_end_date = datetime.strptime(project_end_date, '%Y-%m-%dT%H:%M')
        else:
            project_end_date = None  # Ensure None if not provided

        # Create new lesson
        new_lesson = Lesson(
            user_id=current_user.id,
            project_name=project_name,
            project_description=project_description,
            project_start_date=project_start_date,
            project_end_date=project_end_date,
            project_status=project_status,
            project_phase=project_phase,
            issue_type=issue_type,
            solution=solution,
            recommendation=recommendation,
            tags=tags
        )
        db.session.add(new_lesson)
        db.session.commit()
        return redirect(url_for('main.home'))
    

    return render_template('submit_lesson.html', lesson=Lesson)



@main.route('/lessons')
@login_required
def view_lessons():
    lessons = Lesson.query.order_by(Lesson.id.desc()).all()
    return render_template('view_lessons.html', lessons=lessons)


# @main.route('/analytics')
# @login_required
# def analytics():
#     # Render a template for the analytics page
#     return render_template('analytics.html')

@main.route('/lesson/<int:lesson_id>', methods=['GET'])
@login_required
def view_lesson(lesson_id):
    # Query the lesson by ID
    lesson = Lesson.query.get_or_404(lesson_id)
    # Render a template to display lesson details
    return render_template('view_lesson.html', lesson=lesson)

@main.route('/lesson/<int:lesson_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if request.method == 'POST':
        # Update lesson fields based on form data
        lesson.project_name = request.form['project_name']
        # Other fields can be updated similarly
        db.session.commit()
        flash('Lesson updated!')
        return redirect(url_for('main.profile'))
    return render_template('edit_lesson.html', lesson=lesson)

@main.route('/lesson/<int:lesson_id>/delete', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    flash('Lesson deleted!')
    return redirect(url_for('main.profile'))

@main.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('q', '').strip()
    if not query:
        flash('Please enter a search term.')
        return redirect(request.referrer or url_for('main.home'))

    # Search in Lesson model (adjust the fields as needed)
    lessons = Lesson.query.filter(
        (Lesson.project_name.ilike(f'%{query}%')) |
        (Lesson.issue_type.ilike(f'%{query}%')) |
        (Lesson.tags.ilike(f'%{query}%')) |
        (Lesson.project_description.ilike(f'%{query}%'))
    ).all()

    # Optionally, search in User model
    # users = User.query.filter(
    #     (User.username.ilike(f'%{query}%')) |
    #     (User.full_name.ilike(f'%{query}%')) |
    #     (User.email.ilike(f'%{query}%'))
    # ).all()

    # If the user is not an admin, filter lessons further
    # if not current_user.is_admin:
    #     lessons = lessons.filter_by(user_id=current_user.id)
    # return render_template('search_results.html', query=query, lessons=lessons, users=users)
    return render_template('search_results.html', query=query, lessons=lessons)

@main.route('/analytics', methods=['GET'])
@login_required
def analytics():
    most_common_issues = get_most_common_issues()
    trends_by_phases = get_trends_by_phases()
    issue_trend_chart = generate_issue_trend_chart()
    phase_chart = generate_phase_insights_chart()
    tag_chart = generate_tag_usage_chart()
    status_chart = generate_project_status_chart()
    avg_duration_chart = generate_avg_duration_chart()
    recommendation_wordcloud = generate_recommendation_wordcloud()
    completion_chart = generate_completion_trend_chart()
    scatter_chart = generate_lessons_vs_duration_chart()

    issue_data = {
        "issue_types": [issue[0] for issue in most_common_issues],
        "counts": [issue[1] for issue in most_common_issues],
    }
    phase_data = {
        "phases": [phase[0] for phase in trends_by_phases],
        "counts": [phase[1] for phase in trends_by_phases],
    }

    issue_chart = px.bar(
        x=issue_data["issue_types"], y=issue_data["counts"], 
        title="Most Common Issues", labels={"x": "Issue Type", "y": "Count"}
    ).to_html(full_html=False)

    phase_chart = px.pie(
        names=phase_data["phases"], values=phase_data["counts"], 
        title="Lessons Learned by Project Phase"
    ).to_html(full_html=False)

    return render_template(
    'analytics.html',
    issue_chart=issue_chart,
    issue_trend_chart=issue_trend_chart,
    phase_chart=phase_chart,
    tag_chart=tag_chart,
    status_chart=status_chart,
    avg_duration_chart=avg_duration_chart,
    recommendation_wordcloud=recommendation_wordcloud,
    completion_chart=completion_chart,
    scatter_chart=scatter_chart
)