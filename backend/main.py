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

# Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to frontend folder
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))

# Serve static files like script.js and styles.css
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Serve the index.html page
@app.get("/")
def get_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Load the trained digit recognition model
model = tf.keras.models.load_model("model/digit_model.h5")

# Handle prediction requests
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('L')
    image = image.resize((28, 28))
    image = np.array(image) / 255.0
    image = image.reshape(1, 28, 28, 1)

    prediction = model.predict(image)
    predicted_class = int(np.argmax(prediction))

    return JSONResponse(content={"prediction": predicted_class})
