import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
DUMMY = os.getenv("DUMMY_VAR")

java_result = subprocess.run(["which", "java"], capture_output=True, text=True)

if os.environ.get("JAVA_HOME"):
    print("JAVA_HOME is set")
    java_home = os.environ["JAVA_HOME"]
else:
    print("JAVA_HOME is not set")
    java_home = None

ant_version = subprocess.run(["ant", "-version"], capture_output=True, text=True)

if os.environ.get("ANT_HOME"):
    print("ANT_HOME is set")
    ant_home = os.environ["ANT_HOME"]
else:
    print("ANT_HOME is not set")
    ant_home = None

dist_dpath = Path("/home/souto/Apps/maxprograms/OpenXLIFF/dist")

openxliff_is_installed = True if dist_dpath.exists() else False


app = FastAPI(title="railway-tests")


@app.get("/")  #
def read_root():
    return {
        "java_home": str(java_home),
        "which_java_stdout": str(java_result.stdout.strip()),
        "which_java_stderr": str(java_result.stderr),
        "ant_home": str(ant_home),
        "ant_version_stdout": str(ant_version.stdout.strip()),
        "ant_version_stderr": str(ant_version.stderr),
        "openxliff_is_installed": openxliff_is_installed
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
