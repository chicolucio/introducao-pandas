import pyodbc


class DBManager:
    """
    Adapted from:
    https://github.com/mkleehammer/pyodbc/issues/43#issuecomment-1046678648
    https://stackoverflow.com/a/3783305/8706250
    https://stackoverflow.com/a/38078544/8706250
    """

    def __init__(
        self,
        database,
        driver,
        username=None,
        password=None,
        host=None,
        port=None,
        polling=False,
    ):
        pyodbc.pooling = polling
        self.username = username
        self._password = password
        self.host = host
        self.port = port
        self.database = database
        self.driver = driver
        self._connection = pyodbc.connect(self._create_connection_string())
        self._cursor = self._connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __repr__(self):
        class_name = self.__class__.__name__
        connection_parameters = tuple(self._protected_connection_parameters.values())
        return f"{class_name}{connection_parameters}"

    def __str__(self):
        parameters = self._protected_connection_parameters
        driver = parameters.get("DRIVER")
        database = parameters.get("DATABASE")
        port = parameters.get("PORT", "NO PORT")
        return f"{driver} for {database} on {port}"

    @property
    def _connection_parameters(self):
        parameters = {
            "DATABASE": self.database,
            "DRIVER": self.driver,
            "UID": self.username,
            "PWD": self._password,
            "SERVER": self.host,
            "PORT": self.port,
        }
        return parameters

    def _create_connection_string(self):
        connection_string = ";".join(
            [
                f"{k}={v}"
                for k, v in self._connection_parameters.items()
                if v is not None
            ]
        )
        return connection_string

    @property
    def _protected_connection_parameters(self):
        parameters = {
            k: v for (k, v) in self._connection_parameters.items() if v is not None
        }
        if "PWD" in parameters:
            parameters["PWD"] = "<hidden>"
        return parameters

    @property
    def _protected_connection_string(self):
        connection_string = ";".join(
            [
                f"{k}={v}"
                for k, v in self._protected_connection_parameters.items()
                if v is not None
            ]
        )
        return connection_string

    @property
    def connection(self):
        return self._connection

    def commit(self):
        return self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    @property
    def cursor(self):
        try:
            return self._cursor
        except pyodbc.DatabaseError as err:
            print("DatabaseError {} ".format(err))
            self._cursor.rollback()
            raise err

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
