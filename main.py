from flask import Flask, request, send_file
import pdfplumber
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/crop', methods=['POST'])
def crop_label():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    pdf = pdfplumber.open(file)

    # Use first page
    page = pdf.pages[0]
    im = page.to_image(resolution=300)
    cropped = im.original.crop((0, 600, im.width, 1400))  # Adjust as needed

    output = BytesIO()
    cropped.save(output, format='PNG')
    output.seek(0)

    return send_file(output, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
