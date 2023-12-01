import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

from database.meta import metadata

payment_requests = sa.Table(
    "payment_requests",
    metadata,
    sa.Column(
        "id",
        sa.Integer,
        primary_key=True,
        nullable=False,
    ),
    sa.Column(
        "tid",
        sa.Integer,
        nullable=True,
    ),
    sa.Column(
        "sub_ids",
        ARRAY(sa.String(length=255)),
        nullable=True,
    ),
    sa.Column(
        "inv_ids",
        ARRAY(sa.String(length=255)),
        nullable=True,
    ),
    sa.Column(
        "amt",
        sa.DECIMAL(20, 2),
        nullable=True,
    ),
    sa.Column(
        "curr",
        sa.String(255),
        nullable=True,
    ),
    sa.Column(
        "trn_dat",
        sa.String(255),
        nullable=True,
    ),
    sa.Column(
        "trn_hou",
        sa.Integer,
        nullable=True,
    ),
    sa.Column(
        "cm_amt",
        sa.DECIMAL(20, 2),
        nullable=True,
    ),
    sa.Column(
        "cm_curr",
        sa.DECIMAL(20, 2),
        nullable=True,
    ),
    sa.Column(
        "addl",
        sa.String(1023),
        nullable=True,
    ),
    sa.Column(
        "type",
        sa.String(255),
        nullable=True,
    ),
    sa.Column(
        "response_code",
        sa.Integer,
        nullable=False,
    ),
    sa.Column(
        "status",
        sa.String(255),
        nullable=False,
    ),
    sa.Column(
        "level",
        sa.String(255),
        nullable=False,
    ),
    sa.Column(
        "key",
        sa.String(255),
        nullable=False,
    ),
    sa.Column(
        "dsc",
        ARRAY(sa.String(255)),
        nullable=False,
    ),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=func.now(),    # pylint: disable=not-callable
        nullable=False
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=func.now(),    # pylint: disable=not-callable
        onupdate=func.now(),    # pylint: disable=not-callable
        nullable=False
    ),
)
