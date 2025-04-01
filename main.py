import os
import subprocess

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
DUMMY = os.getenv("DUMMY_VAR")
result = subprocess.run(["which", "java"], capture_output=True, text=True)

app = FastAPI(title="railway-tests")


@app.get("/")  #
def read_root():
    return {
        "java": os.environ["JAVA_HOME"],
        "which_java_stdout": str(result.stdout.strip()),
        "which_java_stderr": str(result.stderr)
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
