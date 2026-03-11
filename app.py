import os
from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
import subprocess

app = Flask(__name__)

# Config Paths
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "scripts" / "generator" / "input"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure input folder exists
if not UPLOAD_FOLDER.exists():
    UPLOAD_FOLDER.mkdir(parents=True)

@app.route('/')
def index():
    # Stable way to list only directories inside the input folder
    tournaments = []
    if UPLOAD_FOLDER.exists():
        for item in UPLOAD_FOLDER.iterdir():
            if item.is_dir():
                tournaments.append(item.name)
    return render_template('index.html', tournaments=tournaments)

@app.route('/upload', methods=['POST'])
def upload_file():
    tournament_name = request.form.get('tournament_name').replace(" ", "_")
    files = request.files.getlist('brochures')

    if not tournament_name or not files:
        return "Missing data", 400

    # Create tournament sub-folder
    t_folder = UPLOAD_FOLDER / tournament_name
    t_folder.mkdir(exist_ok=True)

    # Save all uploaded pages
    for i, file in enumerate(files):
        if file.filename:
            ext = os.path.splitext(file.filename)[1]
            file.save(t_folder / f"page_{i+1}{ext}")

    return redirect(url_for('index'))

@app.route('/run_pipeline')
def run_pipeline():
    # Triggers your existing runner
    subprocess.Popen(["python", "pipeline_runner.py"])
    return "Pipeline Started! Check your console for progress."

if __name__ == '__main__':
    app.run(debug=True, port=5000)