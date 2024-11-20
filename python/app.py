from flask import Flask, jsonify, request
import subprocess
import os
from flask_cors import CORS


app = Flask(__name__)

CORS(app)  # Enable CORS for all origins

@app.route('/process-video', methods=['POST'])
def process_video():
    try:
        # # Handle video file upload
        video_file = request.files['file']
        video_path = './videos/vid.mp4'  # Adjust path as needed
        video_file.save(video_path)
        
        # Process video into images using your existing script
        subprocess.run(['python', 'Youtubers/Ken.py'])
        print("HEYYY")
        return jsonify({'message': 'Video processed into images'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/combine-images', methods=['GET'])
def combine_images():
    try:
        image_folder = './output'
        output_folder = './images/'
        frames_per_combination = 4  # Adjust as needed
        
        # Combine images using your existing script
        subprocess.run(['python', 'combine.py'])

        return jsonify({'message': 'Images combined successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
