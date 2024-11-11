FROM python:3.12.4-slim

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install 

COPY . .

EXPOSE 5000 8501 4200

CMD echo "\n\n __ __  ____  _____  ____  ___   ____  \n|  |  ||    ||     ||    |/   \\ |    \\ \n|  |  | |  | |__/  | |  ||     ||  _  |\n|  |  | |  | |   __| |  ||  O  ||  |  |\n|  :  | |  | |  /  | |  ||     ||  |  |\n \\   /  |  | |     | |  ||     ||  |  |\n  \\_/  |____||_____||____|\\___/ |__|__|\n\n" && poetry run python ./app/app.py