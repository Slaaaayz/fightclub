FROM python


RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libsm6 \
    libxext6 \
    libxrender1 \
    libfontconfig1

RUN pip install pygame
RUN pip install pytmx

WORKDIR /app

COPY . /app

ENV DISPLAY=:0

ENTRYPOINT ["python", "main.py"]

