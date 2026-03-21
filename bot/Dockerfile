FROM python:3.12

WORKDIR /app

COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot ./bot
COPY db ./db

EXPOSE 8501

CMD ["python", "-m", "bot.main.py"]
