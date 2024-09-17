from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
from dotenv import load_dotenv
import io
import os

app = Flask(__name__)

@app.route('/remove', methods=['POST'])
def remove_background():
    load_dotenv()
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Load the image with Pillow
        input_image = Image.open(image_file)

        # Ensure the image is in RGBA mode for transparency
        if input_image.mode != 'RGBA':
            input_image = input_image.convert('RGBA')

        # Use rembg to remove the background
        output_image = remove(input_image)

        # Save the output to a BytesIO object
        img_byte_arr = io.BytesIO()
        
        # Save as PNG (for transparency) with better quality settings
        output_image.save(img_byte_arr, format='PNG', quality=100)
        img_byte_arr.seek(0)

        # Return the processed image
        return send_file(img_byte_arr, mimetype='image/png', as_attachment=True, download_name='output.png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port, debug=False)
