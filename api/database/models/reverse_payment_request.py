import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

from database.meta import metadata

reverse_payment_requests = sa.Table(
    "reverse_payment_requests",
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
