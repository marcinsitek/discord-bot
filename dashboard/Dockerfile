FROM python:3.12

WORKDIR /app

COPY dashboard/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard ./dashboard
COPY db ./db

ENV PYTHONPATH=/app

EXPOSE 8180

CMD ["streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8180"]

