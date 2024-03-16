import logging

import psycopg2


class PostgreSQLPipeline:
    def open_spider(self, spider):
        logging.info('som v pipeline')
        self.connection = psycopg2.connect(
            dbname='mydatabase',
            user='postgres',
            password='password',
            host='db',
            port='5432'
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS flats (
                        title TEXT,
                        image_url TEXT
                    )
                """)
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        sql = "INSERT INTO flats (title, image_url) VALUES (%s, %s)"
        self.cursor.execute(sql, (item['title'], item['image_url']))
        return item
