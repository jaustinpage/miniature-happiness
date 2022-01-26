"""Skeleton init file."""
import sys

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError  # pragma: no cover
    from importlib.metadata import version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError  # pragma: no cover
    from importlib_metadata import version  # pragma: no cover

from flask import Flask

from . import trains

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "miniature-happiness"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # a simple page that says hello
    @app.route("/")
    def root():
        return "OK"

    app.register_blueprint(trains.trains)

    return app
