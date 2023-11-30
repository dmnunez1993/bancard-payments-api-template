import sqlalchemy as sa
from sqlalchemy.sql import func

from database.meta import metadata

invoice_requests = sa.Table(
    "invoice_requests",
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
        nullable=False,
    ),
)
