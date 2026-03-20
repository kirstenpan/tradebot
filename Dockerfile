FROM python:3.9-slim
RUN pip install alpaca-trade-api pandas
COPY bot.py .
CMD ["python", "bot.py"]
