import psycopg2

class PostgresDb(object):
    def __init__(self, host, port, name, user, password, connect=True):
        self.host = host
        self.port = port
        self.name = name
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        if connect:
            self.connect()

    def __str__(self):
        return ' '.join(map(str, [self.host,
                                  self.port,
                                  self.name,
                                  self.user]))

    def connect(self):
        try:
            self.connection = psycopg2.connect(host=self.host,
                                               port=self.port,
                                               user=self.user,
                                               password=self.password,
                                               database=self.name)
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

        except psycopg2.DatabaseError as e:
            print e
            return e.pgerror

    def execute(self, query,  commit=True, repeat=True):
        if self.connection is None:
            self.connect()
        try:
            self.cursor.execute(query)
            if commit:
                self.connection.commit()
        except psycopg2.Error as e:
            print e
            self.connection = None
            return repeat and self.execute(query, commit=commit, repeat=False)
        else:
            return True