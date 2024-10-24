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

CURL
------------
```
curl --location 'http://0.0.0.0:8000/inpaint/' \
--form 'image=@"/E:/ImageInpainting/dg.jpg"' \
--form 'height="400"' \
--form 'width="600"'
```
