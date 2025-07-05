# Medical Imaging AI Maquette

This is a simple Flask web application designed as a maquette (low-fidelity prototype) for a medical imaging AI diagnostic tool. It features a drag-and-drop interface for image uploads, which then simulates or attempts to connect to a Google Cloud Vertex AI model for a diagnostic and precision details.

The application is styled with Tailwind CSS and includes a dark mode.

## Table of Contents

1.  [Prerequisites](https://www.google.com/search?q=%231-prerequisites)
2.  [Google Cloud SDK Setup (for Linux x86\_64)](https://www.google.com/search?q=%232-google-cloud-sdk-setup-for-linux-x86_64)
3.  [Application Setup](https://www.google.com/search?q=%233-application-setup)
4.  [Running the Application](https://www.google.com/search?q=%234-running-the-application)
5.  [Usage](https://www.google.com/search?q=%235-usage)
6.  [Troubleshooting](https://www.google.com/search?q=%236-troubleshooting)

-----

### 1\. Prerequisites

Before you begin, ensure you have the following installed on your system:

  * **Python 3.8+**:

    ```bash
    python3 --version
    ```

  * **pip (Python package installer)**: Usually comes with Python.

    ```bash
    pip --version
    ```

  * **Virtual Environment (`venv`)**: Recommended for managing Python dependencies.

    ```bash
    python3 -m venv --help
    ```

-----

### 2\. Google Cloud SDK Setup (for Linux x86\_64)

This section guides you through installing the Google Cloud SDK and setting up Application Default Credentials (ADC) for your local development environment. ADC allows your application to authenticate with Google Cloud services using your personal Google account's permissions, without needing to download service account keys.

1.  **Download the Google Cloud CLI archive:**

    ```bash
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
    ```

2.  **Extract the archive:**

    ```bash
    tar -xf google-cloud-cli-linux-x86_64.tar.gz
    ```

3.  **Run the installation script:**
    This script adds `gcloud` to your PATH and sets up autocompletion.

    ```bash
    ./google-cloud-sdk/install.sh
    ```

    Follow the prompts. You'll likely be asked if you want to modify your PATH and enable shell command completion. Type `Y` for both.

4.  **Initialize the Google Cloud SDK:**
    This command will guide you through logging into your Google account and selecting a default Google Cloud project.

    ```bash
    ./google-cloud-sdk/bin/gcloud init
    ```

      * It will open a browser for you to log in.
      * You'll be prompted to choose a Google Cloud project. **Select the project where your Vertex AI endpoint is located.**

5.  **Authenticate Application Default Credentials (ADC):**
    This is the crucial step that allows your Python application to find your credentials.

    ```bash
    ./google-cloud-sdk/bin/gcloud auth application-default login
    ```

      * This will open another browser window.
      * Log in with your Google account (the one with `Vertex AI User` permissions in your project).
      * Grant the necessary permissions.

6.  **Verify ADC (Optional):**
    You can confirm that ADC is set up and can obtain an access token:

    ```bash
    ./google-cloud-sdk/bin/gcloud auth application-default print-access-token
    ```

    If this returns a long string, your ADC is correctly configured.

### 3\. Application Setup

1.  **Navigate to your project directory:**
    Assuming you have cloned or downloaded this repository, `cd` into the `python_app` directory.

    ```bash
    cd python_app
    ```

2.  **Create a Python virtual environment:**

    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**

    ```bash
    source venv/bin/activate
    ```

    Your terminal prompt should now show `(venv)` indicating the environment is active.

4.  **Install Python dependencies:**
    You'll need `Flask`, `google-cloud-aiplatform`, and `python-dotenv`.

    ```bash
    pip install Flask google-cloud-aiplatform python-dotenv
    ```

5.  **Create a `.env` file:**
    In the `python_app` directory (the same folder as `app.py`), create a new file named `.env`.

    ```bash
    touch .env
    ```

6.  **Add Vertex AI configuration to `.env`:**
    Open the `.env` file with a text editor and add the following lines, replacing the placeholder values with your actual Vertex AI project ID, region, and endpoint ID.

    ```dotenv
    VERTEX_AI_PROJECT_ID="your-gcp-project-id"
    VERTEX_AI_LOCATION="your-vertex-ai-region" # e.g., us-central1, europe-west4
    VERTEX_AI_ENDPOINT_ID="your-vertex-ai-endpoint-id"
    VERTEX_AI_USE_DEDICATED_ENDPOINT="False" # Set to "True" if you have a dedicated endpoint
    ```

      * **Important:** Ensure no spaces around the `=` sign.
      * **Region:** The `VERTEX_AI_LOCATION` must be one of the [supported Vertex AI regions](https://cloud.google.com/vertex-ai/docs/general/locations).

### 4\. Running the Application

1.  **Ensure your virtual environment is active:**

    ```bash
    source venv/bin/activate
    ```

2.  **Launch the Flask application:**

    ```bash
    python app.py
    ```

    You should see output indicating the Flask development server is running, typically on `http://127.0.0.1:5000/`.

3.  **Open in Browser:**
    Navigate to `http://127.0.0.1:5000/` in your web browser.

### 5\. Usage

  * **Drag & Drop:** Drag an IRM image file from your computer and drop it onto the large square area on the left.
  * **Click to Select:** Alternatively, click the large square area to open a file selection dialog and choose an IRM image.
  * **AI Diagnostic:** The "AI Diagnostic" section on the right will update with a simulated or real (if Vertex AI is configured) diagnostic message.
  * **AI Precision Details:** The "AI Precision Details" section below the drag-and-drop area will provide more context or details from the AI analysis.
  * **Loading Indicator:** A "Analyzing image..." message will appear while the AI is processing the image.

### 6\. Troubleshooting

  * **`ModuleNotFoundError`:**

      * If you see `No module named 'google.cloud'` or `No module named 'dotenv'`, ensure you've activated your virtual environment and run `pip install Flask google-cloud-aiplatform python-dotenv`.

  * **`DefaultCredentialsError`:**

      * This means your application can't authenticate with Google Cloud. Revisit **Step 2.5: Authenticate Application Default Credentials (ADC)**. Ensure you've run `gcloud auth application-default login` and that your Google account has the necessary permissions.

  * **`ValueError: Unsupported region for Vertex AI`:**

      * The `VERTEX_AI_LOCATION` in your `.env` file is incorrect. Check the error message for a list of supported regions and update your `.env` file accordingly. Also, ensure the region matches where your Vertex AI endpoint is actually deployed.

  * **`Status code:500, response: Internal Server Error` from Vertex AI:**

      * This indicates an issue with your deployed Vertex AI model or endpoint itself. You need to check the **Cloud Logging** for your specific Vertex AI endpoint in the Google Cloud Console for detailed error messages. Look for logs around the time you made the prediction request.

  * **`ValueError: Missing Vertex AI configuration`:**

      * Ensure `VERTEX_AI_PROJECT_ID`, `VERTEX_AI_LOCATION`, and `VERTEX_AI_ENDPOINT_ID` are correctly set and not empty in your `.env` file.
