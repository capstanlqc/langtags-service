import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
DUMMY = os.getenv("DUMMY_VAR")

app = FastAPI(title="Langtags API")


@app.get("/")  #
def read_root():
    if DUMMY:
        return {"Hello": DUMMY}
    else:
        return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
