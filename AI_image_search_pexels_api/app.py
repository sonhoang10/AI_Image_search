from flask import Flask, request, jsonify, render_template
import requests
from PIL import Image
from io import BytesIO
import os
from deep_translator import GoogleTranslator

app = Flask(__name__)

PEXELS_API_KEY = "OUYN4wVw1MGPCauACJutekLNWDlCgmt1Juis6OzHlpaajHfZnJqt7b55"

def translate_query(query, dest_lang='en'):
    translator = GoogleTranslator(source='auto', target=dest_lang)
    return translator.translate(query)

def search_images(query):
    translated_query = translate_query(query)
    url = f"https://api.pexels.com/v1/search?query={translated_query}&per_page=5" #chỉnh số lượng tìm kiếm ở đây (5)
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if 'photos' not in data or not data['photos']:
        print("No photos found in the response:", data)
        return []
    
    image_urls = [photo['src']['original'] for photo in data['photos']]
    return image_urls

def download_image(url, path):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search-image', methods=['GET'])
def search_image_route():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    image_urls = search_images(query)
    if not image_urls:
        return jsonify({'error': 'No images found'}), 404
    
    image_paths = []
    for i, image_url in enumerate(image_urls):
        image_path = os.path.join('static', f'{query}_{i}.jpg')
        download_image(image_url, image_path)
        image_paths.append(image_path)
    
    return jsonify({'image_urls': image_paths})

if __name__ == '__main__':
    app.run(debug=True)
