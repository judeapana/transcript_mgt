"""empty message

Revision ID: a52bf520e66d
Revises: d8b3aa28f6c3
Create Date: 2022-03-02 22:15:22.582939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a52bf520e66d'
down_revision = 'd8b3aa28f6c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('grading_system', 'option',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('student', 'first_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('student', 'last_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('student', 'middle_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('user', 'phone_number',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'phone_number',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)
    op.alter_column('student', 'middle_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('student', 'last_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('student', 'first_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('grading_system', 'option',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
