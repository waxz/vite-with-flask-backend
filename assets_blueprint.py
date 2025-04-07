import json
import os
from pathlib import Path

from flask import Blueprint,g, session

# Get environment variables.
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0")
VITE_ORIGIN = os.getenv("VITE_ORIGIN", "http://localhost:8101")

# Set application constants.
is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
is_production = FLASK_DEBUG != "1" or is_gunicorn
project_path = Path(os.path.dirname(os.path.abspath(__file__)))

# Create assets blueprint that stores all Vite-related functionality.
assets_blueprint = Blueprint(
    "assets_blueprint",
    __name__,
    static_folder="assets_compiled/bundled",
    static_url_path="/assets/bundled",
)

# Load manifest file in the production environment.
manifest = {}
if is_production:
    manifest_path = project_path / "assets_compiled/manifest.json"
    try:
        with open(manifest_path, "r") as content:
            manifest = json.load(content)
    except OSError as exception:
        raise OSError(
            f"Manifest file not found at {manifest_path}. Run `npm run build`."
        ) from exception


# Add `asset()` function and `is_production` to app context.
@assets_blueprint.app_context_processor
def add_context():
    def dev_asset(file_path):

        base_url = session["base_url"]
        hostname = session["hostname"]
        print(f"hostname : {hostname}")
        #VITE_ORIGIN = f"http://{hostname}:8101"

        print("VITE_ORIGIN: ", VITE_ORIGIN)
        url = f"{VITE_ORIGIN}/assets/{file_path}"
        print(f"url: {url}")
        return f"{VITE_ORIGIN}/assets/{file_path}"

    def prod_asset(file_path):
        try:
            return f"/assets/{manifest[file_path]['file']}"
        except:
            return "asset-not-found"

    return {
        "asset": prod_asset if is_production else dev_asset,
        "is_production": is_production,
    }
