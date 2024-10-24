Image Inpainting API
=====================================
Overview
------------
The Image Inpainting API is a Python-based API that performs image inpainting to increase image dimensions using generative techniques.

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
![Input Image](https://github.com/fusionsami/ImageInpaintingAPI/blob/main/example_images/postman_api_details.png)

### Input Image:
![Input Image](https://github.com/fusionsami/ImageInpaintingAPI/blob/main/example_images/dog.jpg)

### Output Image:
![Output Image](https://github.com/fusionsami/ImageInpaintingAPI/blob/main/example_images/dog_inpainted.jpg)
