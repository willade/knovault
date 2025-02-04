"""Initialize database

Revision ID: 20303b404a9f
Revises: 
Create Date: 2024-11-12 23:48:58.461241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20303b404a9f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.Column('project_role', sa.String(length=50), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('terms_accepted', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('lesson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('project_name', sa.String(length=100), nullable=False),
    sa.Column('project_phase', sa.String(length=50), nullable=False),
    sa.Column('issue_type', sa.String(length=50), nullable=False),
    sa.Column('solution', sa.Text(), nullable=False),
    sa.Column('recommendation', sa.Text(), nullable=True),
    sa.Column('tags', sa.String(length=100), nullable=True),
    sa.Column('project_description', sa.Text(), nullable=True),
    sa.Column('project_start_date', sa.DateTime(), nullable=True),
    sa.Column('project_end_date', sa.DateTime(), nullable=True),
    sa.Column('project_status', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_lesson_user_id'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lesson')
    op.drop_table('user')
    # ### end Alembic commands ###
