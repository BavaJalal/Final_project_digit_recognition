from tensorflow.keras.datasets import mnist
from PIL import Image
import numpy as np

# Load dataset
(_, _), (x_test, y_test) = mnist.load_data()

# Select one test image (e.g., index 0)
index = 0
img_array = x_test[index]  # shape: (28, 28)
label = y_test[index]

# Convert to PIL image and save
img = Image.fromarray(img_array)
img.save(f"test_digit_{label}_{index}.png")

print(f"Saved image of digit {label} at test_digit_{label}_{index}.png")