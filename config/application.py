"""Application Settings."""

import os
import json

from masonite.environment import env

NAME = env('APP_NAME', 'Survero')

KEY = env("APP_KEY", "-RkDOqXojJIlsF_I8wWiUq_KRZ0PtGWTOZ676u5HtLg=")

HASHING = {
    "default": env("HASHING_FUNCTION", "bcrypt"),
    "bcrypt": {"rounds": 10},
    "argon2": {"memory": 1024, "threads": 2, "time": 2},
}

APP_URL = env("APP_URL", "http://localhost:8000/")

TIME_ZONE = env("TIME_ZONE", "America/New_York")


"""Zotero Path
Path to local PDF files from Zotero 
"""
ZOTERO_PATH = env('ZOTERO_PATH')


"""Tag Group Graphs: Sort Numerically
Which tag groups should be sorted numerically based on content.
For example: ["# of Something: 12", "# of Something: 3", "# of Something: 9"] would be sorted based on [12, 3, 9]. 
"""
if env('TAG_GROUP_GRAPHS__SORT_NUMERICALLY'):
    TAG_GROUP_GRAPHS__SORT_NUMERICALLY = [l for l in env('TAG_GROUP_GRAPHS__SORT_NUMERICALLY').split("\n") if len(l) > 0]
else:
    TAG_GROUP_GRAPHS__SORT_NUMERICALLY = ['']
