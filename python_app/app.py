# app.py
from flask import Flask, render_template, request, jsonify
import os
import base64

# Import Google Cloud Vertex AI client library
from google.cloud import aiplatform
# Import dotenv to load environment variables
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Vertex AI Configuration ---
# Load Vertex AI details from environment variables
PROJECT_ID = os.getenv("VERTEX_AI_PROJECT_ID")
LOCATION = os.getenv("VERTEX_AI_LOCATION")
ENDPOINT_ID = os.getenv("VERTEX_AI_ENDPOINT_ID")
# Convert string from .env to boolean
USE_DEDICATED_ENDPOINT = os.getenv("VERTEX_AI_USE_DEDICATED_ENDPOINT", "False").lower() == "true"

# Validate that environment variables are set
if not all([PROJECT_ID, LOCATION, ENDPOINT_ID]):
    raise ValueError(
        "Missing Vertex AI configuration. Please set VERTEX_AI_PROJECT_ID, "
        "VERTEX_AI_LOCATION, and VERTEX_AI_ENDPOINT_ID in your .env file."
    )

@app.route('/')
def index():
    """Renders the main page of the web application."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handles file uploads and sends the image to a Vertex AI model for processing.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # Read image content as bytes
            image_bytes = file.read()

            # Encode image to base64
            # Vertex AI expects the base64 string without the "data:image/png;base64," prefix
            base64_image = base64.b64encode(image_bytes).decode('utf-8')

            # Define system instruction and prompt for the AI model
            system_instruction = "You are an expert radiologist."
            prompt_text = "Describe this X-ray in detail, focusing on any abnormalities or key observations relevant to a medical diagnostic."

            formatted_prompt = f"{system_instruction} {prompt_text}"

            # Construct the instance payload for Vertex AI
            instances = [
                {
                    "prompt": formatted_prompt,
                    "multi_modal_data": {"image": {"bytes_base64_encoded": base64_image}},
                    "max_output_tokens": 500, # Use max_output_tokens for Gemini models
                    "temperature": 0.2, # A slightly higher temperature for more descriptive output
                    # "raw_response": True, # This parameter might not be directly supported or needed for all Gemini models
                },
            ]

            # Initialize Vertex AI client and endpoint within the request context
            # This ensures the client is fresh for each request, though for performance
            # in production, you might initialize 'client' globally and 'endpoint' once.
            aiplatform.init(project=PROJECT_ID, location=LOCATION)
            endpoint = aiplatform.Endpoint(endpoint_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}")


            # Make the prediction request
            print(f"Sending request to Vertex AI endpoint: {endpoint.resource_name}")
            response = endpoint.predict(instances=instances, parameters={}) # parameters can be an empty dict if not needed

            # Extract the prediction
            if response.predictions and len(response.predictions) > 0:
                # The structure of predictions can vary. For text generation, it's often a string.
                prediction_output = response.predictions[0]

                # Assuming the prediction is directly the diagnostic text
                diagnostic_result = str(prediction_output) # Ensure it's a string

                # For precision, we can state that the diagnostic is detailed
                precision_result = "The AI provided a detailed radiological description based on the image analysis."

                return jsonify({
                    'message': f'File {file.filename} analyzed by AI.',
                    'diagnostic': diagnostic_result,
                    'precision': precision_result,
                    'filename': file.filename
                })
            else:
                return jsonify({
                    'error': 'AI model returned no predictions.',
                    'diagnostic': 'No diagnostic available.',
                    'precision': 'AI model did not provide a valid response.'
                }), 500

        except Exception as e:
            # Log the full error for debugging
            print(f"Error during AI prediction: {e}")
            import traceback
            traceback.print_exc() # Print full traceback to console

            # Fallback or error message for the user
            return jsonify({
                'error': f'Failed to analyze image with AI service. Error: {str(e)}',
                'diagnostic': 'AI analysis failed.',
                'precision': 'Please ensure Vertex AI endpoint is correctly configured and accessible.'
            }), 500
    return jsonify({'error': 'Something went wrong with the upload'}), 500

if __name__ == '__main__':
    app.run(debug=True)

