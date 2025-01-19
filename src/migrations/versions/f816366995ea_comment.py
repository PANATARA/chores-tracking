"""comment

Revision ID: f816366995ea
Revises: dd793837dda1
Create Date: 2025-01-19 12:02:04.593926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f816366995ea'
down_revision: Union[str, None] = 'dd793837dda1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('family',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('family_chore',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('icon', sa.String(), nullable=False),
    sa.Column('valuation', sa.Integer(), nullable=False),
    sa.Column('family_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('username', sa.String(length=60), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surname', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('family_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('family_chore_log',
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('completed_by_id', sa.UUID(), nullable=False),
    sa.Column('chore_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['chore_id'], ['family_chore.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['completed_by_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('icon', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('family_id', sa.UUID(), nullable=False),
    sa.Column('seller_id', sa.UUID(), nullable=True),
    sa.Column('buyer_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['buyer_id'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['seller_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_wallet',
    sa.Column('balance', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wallet_transaction',
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('transaction_type', sa.Enum('purchase', 'income', 'transfer', name='transactiontype'), nullable=False),
    sa.Column('from_user_id', sa.UUID(), nullable=True),
    sa.Column('to_user_id', sa.UUID(), nullable=True),
    sa.Column('product_id', sa.UUID(), nullable=True),
    sa.Column('chore_log_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['chore_log_id'], ['family_chore_log.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['from_user_id'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['to_user_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wallet_transaction')
    op.drop_table('user_wallet')
    op.drop_table('product')
    op.drop_table('family_chore_log')
    op.drop_table('users')
    op.drop_table('family_chore')
    op.drop_table('family')
    # ### end Alembic commands ###
