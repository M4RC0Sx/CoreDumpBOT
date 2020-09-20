import sqlite3


class CoreDumpDB():

    def __init__(self):
        self.conn = sqlite3.connect()
        self.cursor = self.conn.cursor()

    def init_reminders_table(self):

        query = """
        CREATE TABLE coredump_reminders (
            id INT IDENTITY(1,1) PRIMARY KEY,
            author_id BIGINT NOT NULL,
            global BOOLEAN DEFAULT FALSE,
            init_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL,
            name VARCHAR(64) NOT NULL,
            description VARCHAR(256) DEFAULT 'Sin descripción...'
        );
        """

        try:
            self.cursor.execute(query)
            self.conn.commit()

        except Exception as e:
            pass  # TODO - Error control
