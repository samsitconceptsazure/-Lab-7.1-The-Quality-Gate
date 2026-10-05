FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY calculator.py .

CMD ["python", "-c", "from calculator import add, divide; print('Calculator container started'); print('2 + 3 =', add(2, 3)); print('10 / 2 =', divide(10, 2))"]
