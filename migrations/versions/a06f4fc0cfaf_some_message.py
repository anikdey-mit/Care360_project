"""some message

Revision ID: a06f4fc0cfaf
Revises: 29e7e001796e
Create Date: 2020-04-10 22:44:52.498622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a06f4fc0cfaf'
down_revision = '29e7e001796e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('safety_questionnaire', sa.Column('adequate_sunlight', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('bench_height', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('difficulty_bed', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('electrical_cords', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('floor_hazard', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('kid_name', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('kitchen_reach', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('path_checked', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('slip_products', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('stairs_edge', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('stairs_handrails', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('towel_rails', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('unsteady_standing', sa.Text(), nullable=True))
    op.add_column('safety_questionnaire', sa.Column('water_presence', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('safety_questionnaire', 'water_presence')
    op.drop_column('safety_questionnaire', 'unsteady_standing')
    op.drop_column('safety_questionnaire', 'towel_rails')
    op.drop_column('safety_questionnaire', 'stairs_handrails')
    op.drop_column('safety_questionnaire', 'stairs_edge')
    op.drop_column('safety_questionnaire', 'slip_products')
    op.drop_column('safety_questionnaire', 'path_checked')
    op.drop_column('safety_questionnaire', 'kitchen_reach')
    op.drop_column('safety_questionnaire', 'kid_name')
    op.drop_column('safety_questionnaire', 'floor_hazard')
    op.drop_column('safety_questionnaire', 'electrical_cords')
    op.drop_column('safety_questionnaire', 'difficulty_bed')
    op.drop_column('safety_questionnaire', 'bench_height')
    op.drop_column('safety_questionnaire', 'adequate_sunlight')
    # ### end Alembic commands ###