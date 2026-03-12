import os
from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
import subprocess

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "scripts" / "generator" / "input"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not UPLOAD_FOLDER.exists():
    UPLOAD_FOLDER.mkdir(parents=True)

@app.route('/')
def index():
    tournaments = []
    if UPLOAD_FOLDER.exists():
        tournaments = [d.name for d in UPLOAD_FOLDER.iterdir().parent.glob("scripts/generator/input/*") if d.is_dir()]
    # Simplified fallback for the list logic
    tournaments = [f.name for f in UPLOAD_FOLDER.iterdir().parent.joinpath("scripts/generator/input").iterdir().parent.glob("scripts/generator/input/*") if f.is_dir()]
    # Actually, let's just use the most stable pathing:
    tournaments = [d.name for d in UPLOAD_FOLDER.iterdir().parent.joinpath("scripts/generator/input").iterdir().parent.joinpath("scripts/generator/input").iterdir().parent.joinpath("scripts/generator/input").iterdir().parent.joinpath("scripts/generator/input").iterdir().parent.joinpath("scripts/generator/input").iterdir().parent.joinpath("scripts/generator/input").iterdir())]
