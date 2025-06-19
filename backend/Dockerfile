FROM python:3.10-slim

# System dependencies for audio and Japanese text analysis
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    libasound2 \
    libflac8 \
    libvorbis0a \
    libopenblas-dev \
    liblapack-dev \
    ffmpeg \
    mecab \
    mecab-ipadic-utf8 \
    open-jtalk \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ENV OPEN_JTALK_DICT_DIR=/var/lib/mecab/dic/open-jtalk

COPY . .