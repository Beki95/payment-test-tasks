from fastapi import FastAPI


def initialize_app(_app: FastAPI) -> FastAPI:
    return _app


app = initialize_app(
    FastAPI(),
)
