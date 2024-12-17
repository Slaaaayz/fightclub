FROM python

RUN pip install pygame
RUN pip install pytmx

WORKDIR /app

COPY . /app

ENTRYPOINT ["python", "main.py"]

