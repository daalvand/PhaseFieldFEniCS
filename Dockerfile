FROM python

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install pyvista

WORKDIR /app

COPY process_results.py .

CMD ["python", "process_results.py"]
