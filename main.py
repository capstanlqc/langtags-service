import os
import subprocess
import zipfile
import requests

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

def download_file(url, dest_fpath):
    """
    Download a large file with streaming.

    :param url: URL of the file to download.
    :param destination: Path to local version of file that will be written.
    """
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Raise an error for bad HTTP status
            with open(dest_fpath, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  # 8 KB chunks
                    if chunk:  # Filter out keep-alive chunks
                        file.write(chunk)
        # print(f"Download completed: {dest_fpath}")
    except Exception as e:
        # todo: raise exception
        print(f"An error occurred: {e}")


def install_config_bundle(custom_config_url, config_dpath):
    
    os.makedirs(config_dpath, mode=0o777, exist_ok=True)

    def config_is_outdated():
        
        def get_version(line):
            update_pattern = re.compile(r"(\d+)_[csp0]{3}")
            result = update_pattern.search(line.strip())
            return result.group(1)
            
        # check if it has not been installed already
        local_version_fpath = os.path.join(config_dpath, "version_notes.txt")
        if not os.path.isfile(local_version_fpath):
            print("Custom configuration not found, configuration will be installed")
            return True
        
        with open(local_version_fpath, "r") as f:
            # read the first line of the file
            update_line = f.readlines()[2]
            installed_version = get_version(update_line)

        dest_fpath = os.path.join(config_dpath, "index.html")
        download_file(custom_config_url, dest_fpath)

        with open(dest_fpath, "r") as file:
            # read the first line of the file
            update_line = file.readlines()[1]
            available_version = get_version(update_line)
            
        if installed_version < available_version:
            print("Custom configuration is outdated, installing config")
            return True
        
        print("Custom configuration is up to date")
        return

    if not config_is_outdated():
        return config_dpath

    # these urls can be fetched from the file above (index.html)
    config = f"{custom_config_url}/manual/config.zip"
    plugins = f"{custom_config_url}/manual/plugins.zip"
    scrips = f"{custom_config_url}/manual/scripts.zip"

    # config_bundle = "https://github.com/capstanlqc/omegat-user-config-dev572/archive/refs/heads/master.zip"

    #@ download_file
    def fetch_file(url, folder):
        if not os.path.isdir(folder):
            os.makedirs(folder, mode=0o777, exist_ok=True)

        zip_fname = url.split("/")[-1]
        zip_fpath = os.path.join(folder, zip_fname)
        download_file(url, zip_fpath)
        
        with zipfile.ZipFile(zip_fpath, "r") as zip_ref:
            zip_ref.extractall(folder)

        if os.path.isfile(zip_fpath):
            os.remove(zip_fpath)

    fetch_file(config, config_dpath)
    fetch_file(plugins, os.path.join(config_dpath, "plugins"))
    fetch_file(scrips, os.path.join(config_dpath, "scripts"))

    # print(f"save file to '{config_dpath}'")
    # fetch_file(config_bundle, dist_dir)

    required = ["scripts", "plugins", "omegat.prefs", "version_notes.txt"]
    # set(required).issubset(set(os.listdir(config_dpath)))
    if all(item in os.listdir(config_dpath) for item in required):
        return config_dpath
        
        
APP_ROOT = Path.cwd()

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

openxliff_dist_dpath = Path("/app/opt/OpenXLIFF/dist")

openxliff_is_installed = True if openxliff_dist_dpath.exists() else False


omtver="5.7.3"
dist=f"OmegaT_{omtver}_Linux_64"
# dist_pkg=f"{dist}.tar.bz2"
omegat_dist_dpath = os.path.join(APP_ROOT, "opt", "omegat", dist)
java_fpath = os.path.join(APP_ROOT, "opt", "omegat", dist, "jre", "bin", "java")

# omegat jar
omtjar_fpath = os.path.join(APP_ROOT, "opt", "omegat", dist, "OmegaT.jar")

# omegat config
config_dpath = os.path.join(APP_ROOT, "opt", "omegat", "config_dir")
custom_config_url = "https://cat.capstan.be/OmegaT/v572"
config_dpath = install_config_bundle(custom_config_url, config_dpath)

print(f"{omtjar_fpath=}")
print(f"{config_dpath=}")
print(f"{java_fpath=}")

jre11_is_installed = True if Path(java_fpath).exists() else False
omegat_is_installed = True if Path(omtjar_fpath).exists() else False
    

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
        "openxliff_is_installed": openxliff_is_installed,
        "java_fpath": java_fpath,
        "omtjar_fpath": omtjar_fpath,
        "config_dpath": config_dpath,
        "jre11_is_installed": jre11_is_installed,
        "omegat_is_installed": omegat_is_installed
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
