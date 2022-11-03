FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENTRYPOINT ["streamlit", "run", "search_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
