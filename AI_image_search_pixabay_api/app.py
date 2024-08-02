from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
from PIL import Image
from io import BytesIO
from deep_translator import GoogleTranslator

app = Flask(__name__)

PIXABAY_API_KEY = '34619186-7487ffb9418c3be6ba719dd1d'
PIXABAY_API_URL = 'https://pixabay.com/api/'
IMAGE_DIR = 'static/images'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

@app.route('/', methods=['GET', 'POST'])
def index():
    images = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Translate the query from Vietnamese to English
            translated_query = GoogleTranslator(source='vi', target='en').translate(query)
            params = {
                'key': PIXABAY_API_KEY,
                'q': translated_query,
                'image_type': 'photo',
                'per_page': 10
            }
            response = requests.get(PIXABAY_API_URL, params=params)
            data = response.json()
            hits = data.get('hits', [])

            # Download images to the server
            for i, hit in enumerate(hits):
                img_url = hit.get('webformatURL')
                if img_url:
                    img_response = requests.get(img_url)
                    img = Image.open(BytesIO(img_response.content))
                    img_path = os.path.join(IMAGE_DIR, f'image_{i}.png')
                    img.save(img_path)
                    images.append(f'/static/images/image_{i}.png')

    return render_template('index.html', images=images)

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
