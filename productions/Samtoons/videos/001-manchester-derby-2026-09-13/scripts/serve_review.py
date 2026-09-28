"""Local review files with byte-range video seeking; uses installed Flask."""
from pathlib import Path
from flask import Flask, send_from_directory

app = Flask(__name__)
root = Path(__file__).resolve().parents[1]

@app.get('/<path:name>')
def file(name):
    return send_from_directory(root, name, conditional=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8769, threaded=True, debug=False)
