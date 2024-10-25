# Image Inpainting API - Setup and Run Guide
This document provides step-by-step instructions to install and run the Image Inpainting API locally with or without GPU support.

This guide provides instructions on how to run the Image Inpainting API in three different scenarios:
- **Running without Docker**
- **Running with Docker**


# Prerequisites
 - **General Requirements:**
    - Python 3.8 or higher
    - Docker Desktop with WSL 2 support
    - NVIDIA [drivers](https://www.nvidia.com/en-us/drivers/) based on you gpu configurations.

# Clone the Repository:
   ```
   git clone https://github.com/fusionsami/ImageInpaintingAPI.git
   cd ImageInpaintingAPI
   ```
# Project Structure:
   ```
│   .env
│   .gitignore
│   docker-compose.yml
│   Dockerfile
│   Installation.md
│   README.md
│   requirements.txt
│
├───app
│   │   logging_config.py
│   │   main.py
│   │   models.py
│   │   utils.py
│           
├───example_images
│       dog.jpg
│       dog_inpainted.jpg
│       postman_api_details.png
│
└───logs
        error.log
        info.log
        warning.log
   ```

# Running without Docker

### Step 1: Set Up Python Virtual Environment
 - Create a Python virtual environment and activate.
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
### Step 2: Install Dependencies
 - Install requirements.txt and torch with cuda support.
   ```
   pip install -r requirements.txt
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```
### Step 3: Run the Application
 - Once everything is set up, run the FastAPI app using Uvicorn.
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   
# Running with Docker
### Step 3: Run the Application
 - In root directory buid and up using docker-compose.yml file.
   ```
  docker-compose up --build
   ```
