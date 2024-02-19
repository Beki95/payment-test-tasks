import os

import uvicorn
from fastapi import FastAPI


def initialize_app(_app: FastAPI) -> FastAPI:
    return _app


app = initialize_app(
    FastAPI(),
)

if __name__ == "__main__":
    app_name = os.path.basename(__file__).replace(".py", "")
    uvicorn.run(
        app=f"{app_name}:app",
        host="0.0.0.0",
        port=8000,
        workers=1,
        reload=True
    )
