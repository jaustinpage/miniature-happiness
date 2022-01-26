#!/usr/bin/env python3
"""Shim to allow this to work by just executing flask run."""

import miniature_happiness

app = miniature_happiness.create_app()

if __name__ == "__main__":
    app.run()
