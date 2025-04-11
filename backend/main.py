# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from tensorflow.keras.models import load_model
# from PIL import Image, ImageOps
# import numpy as np
# import io

# app = FastAPI()

# # CORS setup
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load your saved model
# model = load_model("model/digit_model.h5")

# # Preprocessing function
# def preprocess_image(image_bytes):
#     img = Image.open(io.BytesIO(image_bytes)).convert("L")  # Convert to grayscale
#     img = ImageOps.invert(img)  # Invert image (black background, white digit)
#     img = img.resize((28, 28))
#     img_array = np.array(img) / 255.0  # Normalize
#     img_array = img_array.reshape(1, 28, 28, 1)
#     return img_array

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     contents = await file.read()
#     try:
#         processed = preprocess_image(contents)
#         prediction = model.predict(processed)
#         predicted_digit = int(np.argmax(prediction))
#         confidence = float(np.max(prediction))
#         return {"digit": predicted_digit, "confidence": confidence}
#     except Exception as e:
#         return {"error": str(e)}

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os

app = FastAPI()

# Enable CORS so the frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files (JS, CSS, etc.)
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Serve the index.html at the root
@app.get("/")
def get_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Load the trained model
model = tf.keras.models.load_model("model/digit_model.h5")

# Prediction endpoint
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('L')
    image = image.resize((28, 28))
    image = np.array(image) / 255.0
    image = image.reshape(1, 28, 28, 1)

    prediction = model.predict(image)
    predicted_class = np.argmax(prediction)

    return JSONResponse(content={"prediction": int(predicted_class)})

