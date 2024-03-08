FROM python:3

RUN apt-get update && apt-get install -y ffmpeg xvfb

RUN pip install pyvista

WORKDIR /app

COPY ProcessResults.py .

CMD ["python", "ProcessResults.py"]
