import sqlalchemy as sa


def add_table_prefix_to_columns(table: sa.Table, prefix=None):
    columns = []

    if prefix is None:
        prefix = table.name

    for el in table.c:
        columns.append(el.label(f"{prefix}.{el.name}"))

    return columns
