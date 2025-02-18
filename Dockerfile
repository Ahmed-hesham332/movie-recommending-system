FROM python:3.12.2-slim-bookworm

WORKDIR /movie-recommending-system

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD ["uvicorn", "src.movies:app", "--host", "0.0.0.0", "--port", "80"]