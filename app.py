from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import nbformat
import papermill as pm
import os
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/mnt/data'
app.config['ALLOWED_EXTENSIONS'] = {'ipynb'}
app.config['STATIC_FOLDER'] = 'static'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Proses notebook yang diunggah
        result = process_notebook(filepath)
        return result
    return redirect(request.url)

def process_notebook(filepath):
    # Tentukan file output sementara
    with tempfile.NamedTemporaryFile(suffix='.ipynb', delete=False) as fout:
        nb_out_path = fout.name
    
    # Jalankan notebook dengan papermill
    pm.execute_notebook(filepath, nb_out_path)
    
    # Baca notebook yang telah dijalankan dan kembalikan keluaran
    with open(nb_out_path, 'r', encoding='utf-8') as fin:
        nb_executed = nbformat.read(fin, as_version=4)
        output = ''
        for cell in nb_executed.cells:
            if 'outputs' in cell:
                for out in cell['outputs']:
                    if out.output_type == 'stream':
                        output += out['text']
                    elif out.output_type == 'execute_result':
                        output += str(out['data']['text/plain'])
                    elif out.output_type == 'error':
                        output += ''.join(out['traceback'])
        os.remove(nb_out_path)
        return f"<h2>Keluaran:</h2><pre>{output}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
