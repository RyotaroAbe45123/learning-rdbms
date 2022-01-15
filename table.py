import psycopg2


class DB(object):
    def __init__(self, db_name: str, user_name: str,
                 schema_name: str = None) -> None:
        self.db_name = db_name
        self.user_name = user_name
        self.schema_name = schema_name

    def begin_connection(self) -> psycopg2.extensions.connection:
        if self.schema_name is not None:
            connect = psycopg2.connect(
                dbname=self.db_name,
                user=self.user_name,
                options=f'-c search_path={self.schema_name}'
            )
        else:
            connect = psycopg2.connect(
                dbname=self.db_name,
                user=self.user_name
            )
        return connect


class Table(DB):
    def __init__(self, db_name: str, user_name: str,
                 schema_name: str, table_name: str = None) -> None:
        super().__init__(
            db_name=db_name, user_name=user_name, schema_name=schema_name
        )
        assert table_name is not None, 'Table name is not defined'
        self.name = table_name

    def insert_data(self, values: tuple):
        with self.begin_connection() as connect:
            with connect.cursor() as cursor:
                print('insertion start')
                try:
                    query = f"insert into {self.name} values {values};"
                    cursor.execute(query)
                    cursor.execute('commit;')
                except psycopg2.errors.UniqueViolation as error:
                    print(error)
                except Exception as error:
                    print(error)
                    cursor.execute('rollback;')
        print('insertion finish')

    def show_all_data(self):
        with self.begin_connection() as connect:
            with connect.cursor() as cursor:
                try:
                    query = f'select * from {self.name}'
                    cursor.execute(query)
                    print('---all data---')
                    print(cursor.fetchall())
                    print('---all data---')
                except Exception as error:
                    print(error)

    def select_data(self, query: str):
        with self.begin_connection() as connect:
            with connect.cursor() as cursor:
                print('selection start')
                try:
                    cursor.execute(query)
                    response = cursor.fetchall()
                except Exception as error:
                    print(error)
        print('selection finish')
        return response
