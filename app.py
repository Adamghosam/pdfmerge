from flask import Flask, render_template, request, send_file
from pypdf import PdfWriter, PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
MERGED_FOLDER = 'merged/'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Render file index.html dari folder templates
    return render_template('index.html')

@app.route('/merge-pdf', methods=['POST'])
def merge_pdf():
    uploaded_files = request.files.getlist("pdfs")
    custom_filename = request.form.get("filename").strip()  # Ambil nama file dari form
    writer = PdfWriter()

    # Simpan file yang diunggah di folder uploads dan tambahkan halaman ke PdfWriter
    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Buka PDF menggunakan PdfReader dan tambahkan setiap halaman ke writer
        reader = PdfReader(file_path)
        for page in reader.pages:
            writer.add_page(page)

    # Pastikan ada nama file, jika tidak ada gunakan nama default
    if not custom_filename:
        custom_filename = "merged_output"
    
    # Pastikan nama file berakhir dengan .pdf
    if not custom_filename.endswith(".pdf"):
        custom_filename += ".pdf"
    
    merged_filepath = os.path.join(MERGED_FOLDER, custom_filename)

    # Simpan PDF yang sudah digabung
    with open(merged_filepath, "wb") as merged_file:
        writer.write(merged_file)

    # Hapus file yang diunggah setelah digunakan (opsional)
    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    # Kirim file hasil gabungan ke pengguna
    return send_file(merged_filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
