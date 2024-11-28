#from app import db
from app.extensions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
#from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id', name='fk_lesson_user_id'))
    project_name = db.Column(db.String(100), nullable=False)
    project_phase = db.Column(db.String(50), nullable=False)
    issue_type = db.Column(db.String(50), nullable=False)
    solution = db.Column(db.Text, nullable=False)
    recommendation = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(100), nullable=True)
    project_description = db.Column(db.Text, nullable=True)
    project_start_date = db.Column(db.DateTime, nullable=True)
    project_end_date = db.Column(db.DateTime, nullable=True)
    project_status = db.Column(db.String(50), nullable=True)  # e.g., "Ongoing", "Completed"

    PROJECT_PHASES = [
        'Initiation Phase',
        'Planning Phase',
        'Execution Phase',
        'Monitoring and Controlling Phase',
        'Closure Phase'
    ]
    ISSUE_TYPES = [
        'Communication Issues',
        'Resource Allocation Issues',
        'Scope Creep',
        'Risk Management',
        'Quality Issues',
        'Stakeholder Alignment',
        'Technical Challenges',
        'Timeline/Deadline Issues',
        'Dependency Management',
        'Budget Overrun',
        'Regulatory or Compliance Issues',
        'Human Resource Issues',
        'Project Governance',
        'Environmental/Social Impact',
        'Others'
    ]
    PROJECT_STATUSES = ['Ongoing', 'Completed', 'On Hold']

    def __repr__(self):
        return f'<Lesson {self.project_name}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)  # Added field for full name
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), default='user')  # 'user' or 'admin'
    project_role = db.Column(db.String(50), nullable=True)  # Optional field for project role
    is_active = db.Column(db.Boolean, default=True)  # Field for account status
    terms_accepted = db.Column(db.Boolean, default=False, nullable=False)  # Field for terms acceptance

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}, Role: {self.role}, Active: {self.is_active}>'
    @property
    def is_admin(self):
        return self.role == 'admin'
