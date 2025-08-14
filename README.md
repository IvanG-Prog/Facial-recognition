## Installing

### Poetry flow

#### Install Poetry

Consult the [official Poetry installation manual](https://python-poetry.org/docs/#installation).

#### Install dependencies in the current environment

```shell
poetry install
```

### Run the Registration process

```shell
poetry run registers
```

### Run the Access process

```shell
poetry run access
```

### Run the Flask application

```shell
poetry run flask
```

This will start the Flask development server, and you can access the application at `http://127.0.0.1:5000/`.

## Linting

```shell
poetry run pylint --recursive=y .
```
