from apiflask import APIFlask
from flask import current_app, redirect, send_from_directory, url_for

from bamboo import blueprints, database, jobs
from bamboo.settings import config


def media_endpoint(filename: str) -> str:
    media_dir = current_app.config["BAMBOO_MEDIA_DIR"]
    max_age = current_app.get_send_file_max_age(filename)
    return send_from_directory(media_dir, filename, max_age=max_age)


def create_app(config_name: str) -> APIFlask:
    app = APIFlask("bamboo", title="Bamboo", version="0.1.0")
    app.config.from_object(config[config_name])

    # blueprints
    blueprints.init_app(app)
    # database
    database.init_app(app)
    # jobs
    jobs.init_app(app)
    # Serve media files for development environment.
    # This will be overriden by nginx in production environment.
    app.add_url_rule(f"{app.config['MEDIA_URL']}/<path:filename>", "media", media_endpoint)

    # TODO: direct it to the dashboard when it's ready.
    @app.get("/")
    def index():
        return redirect(url_for("openapi.docs"))

    return app
