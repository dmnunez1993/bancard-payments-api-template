"""Add invoice and payment requests table

Revision ID: 74d136a07146
Revises: 
Create Date: 2023-12-01 21:14:33.747425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '74d136a07146'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoice_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tid', sa.Integer(), nullable=True),
    sa.Column('addl', sa.String(length=1023), nullable=True),
    sa.Column('sub_ids', postgresql.ARRAY(sa.String(length=255)), nullable=True),
    sa.Column('prd_id', sa.Integer(), nullable=True),
    sa.Column('response_code', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=False),
    sa.Column('level', sa.String(length=255), nullable=False),
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('dsc', postgresql.ARRAY(sa.String(length=255)), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tid', sa.Integer(), nullable=True),
    sa.Column('sub_ids', postgresql.ARRAY(sa.String(length=255)), nullable=True),
    sa.Column('inv_ids', postgresql.ARRAY(sa.String(length=255)), nullable=True),
    sa.Column('amt', sa.DECIMAL(precision=20, scale=2), nullable=True),
    sa.Column('curr', sa.String(length=255), nullable=True),
    sa.Column('trn_dat', sa.String(length=255), nullable=True),
    sa.Column('trn_hou', sa.Integer(), nullable=True),
    sa.Column('cm_amt', sa.DECIMAL(precision=20, scale=2), nullable=True),
    sa.Column('cm_curr', sa.String(length=255), nullable=True),
    sa.Column('addl', sa.String(length=1023), nullable=True),
    sa.Column('type', sa.String(length=255), nullable=True),
    sa.Column('tkt', sa.Integer(), nullable=True),
    sa.Column('aut_cod', sa.Integer(), nullable=True),
    sa.Column('response_code', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=False),
    sa.Column('level', sa.String(length=255), nullable=False),
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('dsc', postgresql.ARRAY(sa.String(length=255)), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment_requests')
    op.drop_table('invoice_requests')
    # ### end Alembic commands ###
