# Import necessary libraries from magic code to build and train a CNN for classifying images of cars and bikes.
import os
import zipfile
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam


# Step 1 Extract the dataset from the downloaded zip file and prepare it for training

dataset_path = r"C:\Users\danny\Downloads\archive-3-1.zip"
extract_path = "dataset"
with zipfile.ZipFile(dataset_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)



train_dir = extract_path


# Step 2  preprocess the data

# Use ImageDataGenerator 
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,  
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    zoom_range=0.15,
    horizontal_flip=True
)


train_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary',
    subset='training'
)


val_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)


# Step 3 Build the CNN model

model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')  
])

model.compile(optimizer=Adam(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.summary()


# Step 4 Train the CNN on the images

history = model.fit(
    train_generator,
    epochs=15,
    validation_data=val_generator
)


# Step 5 Evaluate on 10 test images that i found online and show the predicted labels for each image (car or bike) along with the confidence score.

test_images_path = r"C:\Users\danny\Downloads\archive-3-1\test_images"  

# Load, preprocess, and predict
for img_file in os.listdir(test_images_path):
    img_path = os.path.join(test_images_path, img_file)
    img = load_img(img_path, target_size=(128,128))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array)
    label = "car" if prediction[0][0] > 0.5 else "bike"
    
    plt.imshow(img)
    plt.title(f"Predicted: {label} ({prediction[0][0]:.2f})")
    plt.axis('off')
    plt.show()