from app import db
from app.models import Lesson
from sqlalchemy import func
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Use a non-interactive backend
import matplotlib
matplotlib.use('Agg')

def get_most_common_issues():
    return db.session.query(
        Lesson.issue_type, func.count(Lesson.id).label('count')
    ).group_by(Lesson.issue_type).order_by(func.count(Lesson.id).desc()).limit(5).all()

def get_trends_by_phases():
    return db.session.query(
        Lesson.project_phase, func.count(Lesson.id).label('count')
    ).group_by(Lesson.project_phase).order_by(func.count(Lesson.id).desc()).all()


# Issue Type Breakdown Over Time
def generate_issue_trend_chart():
    issue_trends = db.session.query(
        func.strftime('%Y-%m', Lesson.project_start_date).label('month'),
        Lesson.issue_type,
        func.count(Lesson.id).label('count')
    ).group_by('month', Lesson.issue_type).all()

    df_issues = pd.DataFrame(issue_trends, columns=['month', 'issue_type', 'count'])
    issue_trend_chart = px.line(
        df_issues, 
        x='month', 
        y='count', 
        color='issue_type',
        title='Issue Type Breakdown Over Time',
        labels={'month': 'Month', 'count': 'Count'}
    ).to_html(full_html=False)

    return issue_trend_chart


# Project Phase Insights
def generate_phase_insights_chart():
    phase_data = db.session.query(
        Lesson.project_phase,
        func.count(Lesson.id).label('count')
    ).group_by(Lesson.project_phase).all()

    df_phases = pd.DataFrame(phase_data, columns=['phase', 'count'])
    phase_chart = px.pie(
        df_phases, 
        names='phase', 
        values='count',
        title='Lessons Learned by Project Phase'
    ).to_html(full_html=False)

    return phase_chart


# Tag Usage Analysis
def generate_tag_usage_chart():
    tag_data = db.session.query(
        Lesson.tags, 
        func.count(Lesson.id).label('count')
    ).group_by(Lesson.tags).all()

    df_tags = pd.DataFrame(tag_data, columns=['tags', 'count'])
    tag_chart = px.bar(
        df_tags, 
        x='tags', 
        y='count', 
        title='Tag Usage Analysis',
        labels={'tags': 'Tags', 'count': 'Count'}
    ).to_html(full_html=False)

    return tag_chart


# Project Status Breakdown
def generate_project_status_chart():
    status_data = db.session.query(
        Lesson.project_status, 
        func.count(Lesson.id).label('count')
    ).group_by(Lesson.project_status).all()

    df_status = pd.DataFrame(status_data, columns=['status', 'count'])
    status_chart = px.pie(
        df_status, 
        names='status', 
        values='count',
        title='Project Status Breakdown'
    ).to_html(full_html=False)

    return status_chart


# Average Project Duration by Status
def generate_avg_duration_chart():
    duration_data = db.session.query(
        Lesson.project_status,
        func.avg(func.julianday(Lesson.project_end_date) - func.julianday(Lesson.project_start_date)).label('avg_duration')
    ).group_by(Lesson.project_status).all()

    df_duration = pd.DataFrame(duration_data, columns=['status', 'avg_duration'])
    duration_chart = px.bar(
        df_duration, 
        x='status', 
        y='avg_duration', 
        title='Average Project Duration by Status',
        labels={'status': 'Project Status', 'avg_duration': 'Average Duration (Days)'}
    ).to_html(full_html=False)

    return duration_chart


# Top Recommendations
def generate_recommendation_wordcloud():
    recommendations = db.session.query(Lesson.recommendation).all()
    text = " ".join([rec[0] for rec in recommendations])

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    img = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    img_base64 = base64.b64encode(img.getvalue()).decode()
    return f'data:image/png;base64,{img_base64}'


# Completion Trends Over Time
def generate_completion_trend_chart():
    completion_trends = db.session.query(
        func.strftime('%Y-%m', Lesson.project_end_date).label('month'),
        func.count(Lesson.id).label('count')
    ).group_by('month').all()

    df_completion = pd.DataFrame(completion_trends, columns=['month', 'count'])
    completion_chart = px.line(
        df_completion, 
        x='month', 
        y='count', 
        title='Completion Trends Over Time',
        labels={'month': 'Month', 'count': 'Count'}
    ).to_html(full_html=False)

    return completion_chart


# Lessons Learned vs. Project Duration
def generate_lessons_vs_duration_chart():
    lessons_data = db.session.query(
        func.julianday(Lesson.project_end_date) - func.julianday(Lesson.project_start_date),
        func.count(Lesson.id).label('lesson_count')
    ).group_by(Lesson.id).all()

    df_lessons = pd.DataFrame(lessons_data, columns=['duration', 'lesson_count'])
    scatter_chart = px.scatter(
        df_lessons, 
        x='duration', 
        y='lesson_count',
        title='Lessons Learned vs. Project Duration',
        labels={'duration': 'Project Duration (Days)', 'lesson_count': 'Lessons Learned'}
    ).to_html(full_html=False)

    return scatter_chart