FROM python:3.12-bullseye

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install

COPY src/ ./src/
COPY workers/ ./workers/

ENV PYTHONPATH=/app

CMD ["poetry", "run", "python", "workers/book_rental_notification_worker.py"]