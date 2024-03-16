FROM python:3.12

WORKDIR /app

COPY uloha /app

RUN pip install --no-cache-dir scrapy psycopg2 selenium fake-useragent

#RUN apt-get update && apt-get install -y \
 #   x11vnc \
  #  xvfb \
   # xterm \
    #fluxbox \
    #&& rm -rf /var/lib/apt/lists/*

# RUN mkdir ~/.vnc
# RUN x11vnc -storepasswd your_password ~/.vnc/passwd

#CMD ["x11vnc", "-forever", "-usepw", "-create"]

EXPOSE 8080

CMD ["python", "simple_server.py"]
