FROM python:3.14

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .
RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["python", "-m", "uvicorn", "internet_shop.main:app", "--host", "0.0.0.0", "--port", "8000"]
