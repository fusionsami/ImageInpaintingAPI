Image Inpainting API
=====================================
Overview
------------
The Image Inpainting API is a Python-based API that utilizes the Hugging Face diffusers library to perform image inpainting using state-of-the-art models. Specifically, this API employs the Deep Image Inpainting model(runwayml/stable-diffusion-inpaintin), which is fine-tuned for image completion tasks.
The API is built using FastAPI and utilizes the PyTorch library for efficient model inference. 

The inpainting process is executed via a pipeline (pipe) that integrates the following components:
- **Image Preprocessing:** Handles image resizing, normalization, and formatting.
- **Deep Image Inpainting Model:** Performs image completion using the Hugging Face model like runwayml/stable-diffusion-inpaintin.
- **Post-processing:** Converts the output to the desired image format.

API Details
------------
- **Endpoint:** /inpaint
- **Method:** POST
- **Request Body:**
  - **image:** Image file (required)
  - **height:** Integer (required)
  - **width:** Integer (required)

- **Response:**
  - **inpainted_image:** Inpainted image file
  - **status:** Success status (200 OK)
- **Request/Response Formats:**
  - **Request:** multipart/form-data
  - **Response:** image/jpeg

Validation Notes
------------------
- **Image File:**
  - Must be provided.
  - Must not be empty.
  - Supported formats: JPEG, PNG.
    
- **Width and Height:**
  - Must be positive integers.
  - Must be divisible by 8.
 
Error Details
----------------
- **400 Bad Request:** Invalid request format.
- **422 Validation Error:** Invalid image file or dimensions.
- **500 Internal Server Error:** Server-side error.
  
CURL
------------
```
curl --location 'http://0.0.0.0:8000/inpaint/' \
--form 'image=@"/E:/ImageInpainting/dg.jpg"' \
--form 'height="400"' \
--form 'width="600"'
```

Example
----------------

### API:
![Input Image](./example_images/postman_api_details.png)

### Input Image:
![Input Image](./example_images/dog.jpg)

### Output Image:
![Output Image](./example_images/dog_inpainted.jpg)


Limitations and Notes
-----------------------
- **Accuracy Variability:** Due to the complexity of image inpainting tasks, the API may not always produce accurate results. In such cases, requesting multiple times may yield better outcomes.
- **Request Retry:** If the initial response is not satisfactory, clients may need to re-request the inpainting process to achieve desired results.

Installation
-----------------------
- Refer to the [Installation.md](./Installation.md) file for setup and installation instructions.
