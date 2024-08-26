from flask import Flask, request, jsonify, send_file, abort
import pandas as pd
from csv_operations import get_csv_data, save_csv_data, append_to_csv

app = Flask(__name__)

@app.route('/csv/<file_name>', methods=['GET'])
def get_csv(file_name):
    try:
        data = get_csv_data(file_name)
        return data.to_json(orient='records')
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/csv/<file_name>', methods=['POST'])
def upload_csv(file_name):
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file.save(f"data/{file_name}")
    return jsonify({"message": f"File {file_name} uploaded successfully"}), 201

@app.route('/csv/<file_name>/append', methods=['POST'])
def append_csv(file_name):
    try:
        row = request.get_json()
        if not row:
            return jsonify({"error": "No data provided"}), 400
        append_to_csv(file_name, row)
        return jsonify({"message": f"Row appended to {file_name} successfully"}), 200
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/csv/<file_name>/download', methods=['GET'])
def download_csv(file_name):
    try:
        file_path = f"data/{file_name}"
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
