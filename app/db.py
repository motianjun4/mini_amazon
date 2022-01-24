from sqlalchemy import create_engine, text


class DB:
    """Hosts all functions for querying the database.

    Use the execute() method if you want to execute a single SQL
    statement (which will be in a transaction by itself.

    If you want to execute multiple SQL statements in the same
    transaction, use the following pattern:

    >>> with app.db.engine.begin() as conn:
    >>>     # everything in this block executes as one transaction
    >>>     value = conn.execute(text('SELECT...'), bar='foo').first()[0]
    >>>     conn.execute(text('INSERT...'), par=value)
    >>>     conn.execute(text('UPDATE...'), par=value)
    >>>

    """
    def __init__(self, app):
        self.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                                    execution_options={"isolation_level": "SERIALIZABLE"})

    def execute(self, sqlstr, **kwargs):
        """Execute a single SQL statement sqlstr.
        If the statement is a query or a modification with a RETURNING clause,
        return the list of result tuples;
        if the statement is an UPDATE or DELETE statement without RETURNING,
        return the rows matched by the WHERE criterion of the UPDATE or DELETE statement;
        otherwise, return None.
        An exception will be raised for any error encountered.
        sqlstr will be wrapped automatically in a sqlalchemy.sql.expression.TextClause.
        You can use :param inside sqlstr and supply its value as a kwarg.  See
        https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.execute
        https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text
        https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.CursorResult
        for additional details.  See models/*.py for examples of
        calling this function.
        """
        with self.engine.begin() as conn:
            result = conn.execute(text(sqlstr), kwargs)
            if result.returns_rows:
                return result.fetchall()
            else:
                return result.rowcount
