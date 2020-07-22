FROM python:3.6-slim

RUN apt-get update
RUN apt-get install -y wget xfonts-75dpi xfonts-base fontconfig libjpeg62-turbo libx11-6 libxcb1 libxext6 libxrender1
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.stretch_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6-1.stretch_amd64.deb

WORKDIR /app

RUN mkdir Temp

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./startBot.py" ]