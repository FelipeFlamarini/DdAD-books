FROM python:3.12-bullseye

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install

COPY src/ ./src/

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["poetry", "run", "fastapi", "run", "src/app.py", "--host", "0.0.0.0", "--port", "8000"]