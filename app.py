from flask import Flask, jsonify, render_template
import nbformat
import matplotlib.pyplot as plt

app = Flask(__name__)

def extract_report_from_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    accuracy = None
    report = None
    
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            source = cell.source
            if "accuracy =" in source and "classification_report" in source:
                # Execute the cell content to extract variables
                exec(source, globals())
                accuracy = globals().get('accuracy')
                report = globals().get('report')
                break
    
    return accuracy, report

@app.route('/')
def index():
    return render_template('report.html')

@app.route('/data')
def data():
    chart_data = {
        "labels": ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        "datasets": [{
            "label": "# of Votes",
            "data": [12, 19, 3, 5, 2, 3],
            "backgroundColor": [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            "borderColor": [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            "borderWidth": 1
        }]
    }
    return jsonify(chart_data)

@app.route('/report')
def report():
    notebook_path = "71220953_Yeremia-Christopher_Prediksi-Viral-Konten-Sosmed_Classification.ipynb"
    accuracy, report = extract_report_from_notebook(notebook_path)
    accuracy = 0.6315623521992748
    precision = [0.61, 0.65]
    recall = [0.57, 0.69]
    f1_score = [0.59, 0.67]

    # Membuat grafik batang
    plt.figure(figsize=(10, 6))
    x = ['Akurasi', 'Precision (Kelas 0)', 'Precision (Kelas 1)', 'Recall (Kelas 0)', 'Recall (Kelas 1)', 'F1-Score (Kelas 0)', 'F1-Score (Kelas 1)']
    y = [accuracy] + precision + recall + f1_score
    plt.bar(x, y, color=['blue', 'green', 'green', 'orange', 'orange', 'red', 'red'])
    plt.xlabel('Metrik')
    plt.ylabel('Nilai')
    plt.title('Hasil Evaluasi Model Klasifikasi')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Menampilkan grafik
    plt.show()

if __name__ == '__main__':
    app.run(debug=True)
