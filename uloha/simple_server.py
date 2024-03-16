import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import psycopg2
import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.quotes_spider import SrealitySpider


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            num_items = self.count_items_in_database()
            if num_items == 0:
                self.run_scraper()
                time.sleep(10)

            items = self.fetch_items_from_database()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.generate_html(items).encode())
        except Exception as e:
            self.send_error(500, f'Internal Server Error: {str(e)}')


    def count_items_in_database(self):
        connection = psycopg2.connect(
            dbname='mydatabase',
            user='postgres',
            password='password',
            host='db',
            port='5432'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'flats')")
        table_exists = cursor.fetchone()[0]

        if table_exists:
            cursor.execute("SELECT COUNT(*) FROM flats")
            num_items = cursor.fetchone()[0]
        else:
            num_items = 0

        cursor.close()
        connection.close()
        return num_items


    def fetch_items_from_database(self):
        connection = psycopg2.connect(
            dbname='mydatabase',
            user='postgres',
            password='password',
            host='db',
            port='5432'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT title, image_url FROM flats")
        items = [{'title': title, 'image_url': image_url} for title, image_url in cursor.fetchall()]
        cursor.close()
        connection.close()
        return items

    def run_scraper(self):
        process = CrawlerProcess(get_project_settings())
        process.crawl(SrealitySpider)
        process.start()

    def generate_html(self, items):
        html = """
            <!doctype html>
            <html>
            <head><title>Scraped Flats</title></head>
            <body>
            <h1>Scraped Flats</h1>
            <div id="flats"></div>
            <script>
                var items = %s;
                const flatsDiv = document.getElementById('flats');
                items.forEach(item => {
                    const flat = document.createElement('div');
                    flat.innerHTML = `<h2>${item.title}</h2><img src="${item.image_url}" width="300" height="200"/>`;
                    flatsDiv.appendChild(flat);
                });
            </script>
            </body>
            </html>
        """ % json.dumps(items)
        return html


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
