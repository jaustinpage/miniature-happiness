"""Shim to allow this to work by just executing flask run."""

from src.miniature_happiness import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()
