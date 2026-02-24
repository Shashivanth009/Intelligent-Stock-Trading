import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
from main import run_simulation
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configure upload folder
UPLOAD_FOLDER = 'data/uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "filename": filename, "filepath": filepath})

    return jsonify({"error": "Invalid file type. Only CSV files are allowed."}), 400

@app.route('/api/train', methods=['POST'])
def train_model():
    try:
        data = request.json

        filepath = data.get('filepath') or 'data/stock_data.csv'

        if not os.path.exists(filepath):
            return jsonify({"error": f"Data file not found: '{filepath}'. Please upload a CSV file."}), 400

        epochs = int(data.get('epochs', 3))
        window = int(data.get('window_size', 10))
        initial_balance = float(data.get('initial_balance', 10000))

        results = run_simulation(
            data_path=filepath,
            epochs=epochs,
            window=window,
            initial_balance=initial_balance
        )

        return jsonify(results)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode)
