import numpy as np
from PIL import Image, ImageEnhance
import os
import cv2

def growth_and_spread(image_array, intensity=1.5):
    """
    Apply a "growth and spread" effect that amplifies color intensity
    and expands details in the image for a surreal transformation.
    """
    # Erhöhe Kontrast und Helligkeit, um einen "wachsenden" Effekt zu erzeugen
    img = Image.fromarray(image_array)
    enhancer_brightness = ImageEnhance.Brightness(img)
    enhancer_contrast = ImageEnhance.Contrast(img)
    
    # Wachstums- und Ausbreitungseffekt durch Anpassung der Helligkeit und des Kontrasts
    img = enhancer_brightness.enhance(1 + 0.2 * intensity)
    img = enhancer_contrast.enhance(1 + 0.3 * intensity)

    # Erweiterung durch leichte Unschärfe und Schärfung
    img_cv = np.array(img)
    blurred = cv2.GaussianBlur(img_cv, (7, 7), 0)
    sharpened = cv2.addWeighted(img_cv, 1.5, blurred, -0.5, 0)

    # Leichter Farbverschiebungseffekt
    hsv_image = cv2.cvtColor(sharpened, cv2.COLOR_RGB2HSV)
    hsv_image[:, :, 0] = (hsv_image[:, :, 0] + int(10 * intensity)) % 180
    transformed_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
    
    return transformed_image

def save_frames_with_growth_and_spread(input_image_path, output_folder, duration_seconds=10, fps=24, initial_intensity=1.0, intensity_step=0.1):
    """
    Applies the growth_and_spread effect to an image and saves a sequence of frames.
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
        
        # Wende den Wachstumseffekt an
        transformed_image = growth_and_spread(img_array, intensity=intensity)
        
        # Speichere den Frame
        frame_path = os.path.join(output_folder, f"frame_{i:04d}.jpg")
        
        # Explizite Speicherung und Ausgabe zur Bestätigung
        Image.fromarray(transformed_image).save(frame_path)
        print(f"Frame {i:04d} gespeichert unter {frame_path} mit Intensität {intensity:.2f}")

# Beispielaufruf
save_frames_with_growth_and_spread("image.jpg", "output_frames/growth_and_spread", duration_seconds=10, fps=24, initial_intensity=1.0, intensity_step=0.02)
