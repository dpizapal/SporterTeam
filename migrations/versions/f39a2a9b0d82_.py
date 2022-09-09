"""empty message

<<<<<<<< HEAD:migrations/versions/f39a2a9b0d82_.py
Revision ID: f39a2a9b0d82
Revises: 
Create Date: 2022-09-05 16:49:35.223027
========
Revision ID: ac570d1e9496
Revises: 
Create Date: 2022-09-05 15:19:19.824593
>>>>>>>> origin/Develop:migrations/versions/ac570d1e9496_.py

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
<<<<<<<< HEAD:migrations/versions/f39a2a9b0d82_.py
revision = 'f39a2a9b0d82'
========
revision = 'ac570d1e9496'
>>>>>>>> origin/Develop:migrations/versions/ac570d1e9496_.py
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=80), nullable=True),
    sa.Column('profile_image_url', sa.String(length=250), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('evento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sport', sa.String(length=250), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('agemin', sa.Integer(), nullable=True),
    sa.Column('agemax', sa.Integer(), nullable=True),
    sa.Column('payment', sa.Integer(), nullable=False),
    sa.Column('space', sa.Boolean(), nullable=False),
    sa.Column('participantmax', sa.Integer(), nullable=True),
    sa.Column('ciudad', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('admin', sa.Integer(), nullable=True),
    sa.Column('estadoEvento', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['admin'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('evento_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['evento_id'], ['evento.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'evento_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('participant')
    op.drop_table('evento')
    op.drop_table('user')
    # ### end Alembic commands ###
