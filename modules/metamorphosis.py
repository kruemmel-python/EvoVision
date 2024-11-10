import numpy as np
from PIL import Image, ImageEnhance
import os
import cv2

def metamorphosis(image_array, distortion_intensity=0.005, color_shift_intensity=0.5):
    """
    Apply a "metamorphosis" effect by gradually distorting and shifting colors
    to create a surreal transformation effect.
    """
    rows, cols, _ = image_array.shape

    # Erzeuge Verzerrungseffekte basierend auf Sinuswellen
    x_distortion = (distortion_intensity * np.sin(np.linspace(0, 3 * np.pi, cols))).astype(np.float32)
    y_distortion = (distortion_intensity * np.cos(np.linspace(0, 3 * np.pi, rows))).astype(np.float32)

    # Erzeuge Meshgrids, um die Verzerrung anzuwenden
    x = np.arange(cols)
    y = np.arange(rows)
    x_grid, y_grid = np.meshgrid(x, y)

    # Wende die Verzerrung an
    map_x = (x_grid + x_distortion).astype(np.float32)
    map_y = (y_grid + y_distortion[:, np.newaxis]).astype(np.float32)
    distorted_image = cv2.remap(image_array, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    # Farbverschiebung
    hsv_image = cv2.cvtColor(distorted_image, cv2.COLOR_RGB2HSV)
    hsv_image[:, :, 0] = (hsv_image[:, :, 0] + int(color_shift_intensity * 30)) % 180  # Farbe ändern
    transformed_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
    
    return transformed_image

def save_frames_with_metamorphosis(input_image_path, output_folder, duration_seconds=10, fps=24, initial_distortion_intensity=0.005, distortion_step=0.001, color_shift_intensity=0.5):
    """
    Applies the metamorphosis effect to an image and saves a sequence of frames.
    """
    # Lade das Bild
    img = Image.open(input_image_path).convert("RGB")
    img_array = np.array(img)

    # Erstelle das Ausgabeverzeichnis, falls es nicht existiert
    os.makedirs(output_folder, exist_ok=True)

    # Berechne die Anzahl der Frames basierend auf Dauer und FPS
    num_frames = duration_seconds * fps

    for i in range(num_frames):
        # Berechne die Intensität für Verzerrung und Farbverschiebung für diesen Frame
        distortion_intensity = initial_distortion_intensity + i * distortion_step
        
        # Wende den Metamorphose-Effekt an
        transformed_image = metamorphosis(img_array, distortion_intensity=distortion_intensity, color_shift_intensity=color_shift_intensity)
        
        # Speichere den Frame
        frame_path = os.path.join(output_folder, f"frame_{i:04d}.jpg")
        
        # Speichere explizit jeden Frame und gebe den Status in der Konsole aus
        Image.fromarray(transformed_image).save(frame_path)
        print(f"Frame {i:04d} gespeichert unter {frame_path} mit Distortion Intensity {distortion_intensity:.5f}")

# Beispielaufruf
save_frames_with_metamorphosis("image.jpg", "output_frames/metamorphosis", duration_seconds=10, fps=24, initial_distortion_intensity=0.005, distortion_step=0.001, color_shift_intensity=0.5)
