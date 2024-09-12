from flask import Flask, request, jsonify
from openai import OpenAI
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允許所有來源

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    user_prompt = data.get('prompt')

    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Prepend the coin design instruction to the user's prompt
    full_prompt = f"Please generate a coin design picture. My topic is: {user_prompt}"

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return jsonify({"image_url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

