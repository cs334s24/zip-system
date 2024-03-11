# app.py
from flask import Flask, render_template, request
from zip import getFileIdsFromUser, searchFilesWithIds, zipSampleData, main

def get_file_ids_from_user():
    return [id.strip() for id in ids.split(',')]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    file_ids = request.args.get('file_ids')
    if file_ids:
        file_ids = get_file_ids_from_user(file_ids)
        files = searchFilesWithIds(file_ids)
        return render_template('search.html', files=files)
    else:
        return "No file ids provided"

if __name__ == "__main__":
    app.run(debug=True)
