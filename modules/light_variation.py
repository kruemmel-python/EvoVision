import numpy as np
from PIL import Image, ImageEnhance
import os
import cv2

def light_variation(image_array, intensity=1.0):
    """
    Apply a "light variation" effect that adjusts brightness and adds a warm or cool tone,
    simulating dynamic lighting conditions.
    """
    # Passe Helligkeit und Kontrast an, um Lichtvariationen zu simulieren
    img = Image.fromarray(image_array)
    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(1 + 0.2 * intensity)

    # Konvertiere zu OpenCV-Format, um Farbverschiebung anzuwenden
    img_cv = np.array(img)

    # Erzeuge eine Farbverschiebung, indem wir den Blau- und Rotkanal anpassen
    # für warmes oder kühles Licht
    shift = int(20 * intensity)
    img_cv[:, :, 0] = np.clip(img_cv[:, :, 0] + shift, 0, 255)  # Blau-Kanal
    img_cv[:, :, 2] = np.clip(img_cv[:, :, 2] - shift, 0, 255)  # Rot-Kanal
    
    return img_cv

def save_frames_with_light_variation(input_image_path, output_folder, duration_seconds=10, fps=24, initial_intensity=1.0, intensity_step=0.05):
    """
    Applies the light_variation effect to an image and saves a sequence of frames.
    """
    # Lade das Bild
    img = Image.open(input_image_path).convert("RGB")
    img_array = np.array(img)

    # Erstelle das Ausgabeverzeichnis, falls es nicht existiert
    os.makedirs(output_folder, exist_ok=True)

    # Berechne die benötigte Anzahl der Frames basierend auf Dauer und FPS
    num_frames = duration_seconds * fps

    for i in range(num_frames):
        # Berechne die Intensität für diesen Frame
        intensity = initial_intensity + i * intensity_step
        
        # Wende den Lichteffekt an
        transformed_image = light_variation(img_array, intensity=intensity)
        
        # Speichere den Frame
        frame_path = os.path.join(output_folder, f"frame_{i:04d}.jpg")
        
        # Speichere explizit jeden Frame und gebe den Status in der Konsole aus
        Image.fromarray(transformed_image).save(frame_path)
        print(f"Frame {i:04d} gespeichert unter {frame_path} mit Intensität {intensity:.2f}")

# Beispielaufruf
save_frames_with_light_variation("image.jpg", "output_frames/light_variation", duration_seconds=10, fps=24, initial_intensity=1.0, intensity_step=0.05)
