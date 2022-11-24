FROM python:3.7
COPY requirements.txt requirements.txt
RUN pip install -r /app/requirements.txt
COPY . .
CMD python main.py
