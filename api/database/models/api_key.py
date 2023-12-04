import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

from database.meta import metadata

api_keys = sa.Table(
    "api_keys",
    metadata,
    sa.Column(
        "id",
        sa.Integer,
        primary_key=True,
        nullable=False,
    ),
    sa.Column(
        "name",
        sa.String(255),
        nullable=False,
    ),
    sa.Column(
        "prefix",
        sa.String(255),
        nullable=False,
    ),
    sa.Column(
        "hashed_key",
        sa.String(255),
        nullable=False,
    ),
    sa.Column(
        "permissions",
        ARRAY(sa.String(length=255)),
        nullable=False,
    ),
    sa.Column(
        "is_active",
        sa.Integer,
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
