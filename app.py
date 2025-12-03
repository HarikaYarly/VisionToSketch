import os
from flask import Flask, request, render_template, send_file, url_for

app = Flask(__name__)

def convert_to_sketch(input_path, output_path):
    import cv2
    image = cv2.imread(input_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    inverted = 255 - gray
    blur = cv2.GaussianBlur(inverted, (25, 25), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    cv2.imwrite(output_path, sketch)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        input_path = 'input' + os.path.splitext(f.filename)[1]
        output_path = 'static/sketch.png'
        f.save(input_path)
        convert_to_sketch(input_path, output_path)
        return render_template('preview.html', sketch_url=url_for('static', filename='sketch.png'))
    return render_template('upload.html')

@app.route('/download')
def download_sketch():
    return send_file('static/sketch.png', mimetype='image/png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
