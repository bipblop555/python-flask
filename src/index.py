from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

def convert_image_to_pdf(image):
    temp_filename = 'temp_image.png'
    Image.open(image).save(temp_filename)

    pdf_data = BytesIO()
    pdf = canvas.Canvas(pdf_data)
    pdf.drawImage(temp_filename, 10, 10, width=180, height=180)
    pdf.save()

    os.remove(temp_filename)

    return pdf_data.getvalue()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(url_for('index'))

    image = request.files['image']

    if image.filename == '':
        return redirect(url_for('index'))

    if image and image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        pdf_data = convert_image_to_pdf(image)

        return send_file(BytesIO(pdf_data), download_name='output.pdf', as_attachment=True, mimetype='application/pdf')
    else:
        return "Le fichier téléchargé n'est pas une image valide."


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
