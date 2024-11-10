import numpy as np
from PIL import Image
import os
import cv2

def organic_movement(image_array, wave_intensity=5, frequency=0.1):
    """
    Apply an "organic movement" effect that simulates fluid, wave-like distortions in the image.
    """
    rows, cols, _ = image_array.shape

    # Erzeuge eine Meshgrid, das für die Transformation verwendet wird
    x = np.arange(cols)
    y = np.arange(rows)
    x_grid, y_grid = np.meshgrid(x, y)

    # Simuliere eine wellenartige Verzerrung basierend auf Sinuswellen
    x_offset = (wave_intensity * np.sin(2 * np.pi * frequency * y_grid)).astype(np.float32)
    y_offset = (wave_intensity * np.cos(2 * np.pi * frequency * x_grid)).astype(np.float32)

    # Wende die Verzerrung auf das Bild an
    map_x = (x_grid + x_offset).astype(np.float32)
    map_y = (y_grid + y_offset).astype(np.float32)
    transformed_image = cv2.remap(image_array, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    return transformed_image

def save_frames_with_organic_movement(input_image_path, output_folder, duration_seconds=10, fps=24, initial_wave_intensity=5, wave_intensity_step=0.1, frequency=0.1):
    """
    Applies the organic_movement effect to an image and saves a sequence of frames.
    """
    # Lade das Bild
    img = Image.open(input_image_path).convert("RGB")
    img_array = np.array(img)

    # Erstelle das Ausgabeverzeichnis, falls es nicht existiert
    os.makedirs(output_folder, exist_ok=True)

    # Berechne die Anzahl der Frames basierend auf Dauer und FPS
    num_frames = duration_seconds * fps

    for i in range(num_frames):
        # Berechne die Intensität der Wellenbewegung für diesen Frame
        wave_intensity = initial_wave_intensity + i * wave_intensity_step
        
        # Wende den organischen Bewegungseffekt an
        transformed_image = organic_movement(img_array, wave_intensity=wave_intensity, frequency=frequency)
        
        # Speichere den Frame
        frame_path = os.path.join(output_folder, f"frame_{i:04d}.jpg")
        
        # Speichere explizit jeden Frame und gebe den Status in der Konsole aus
        Image.fromarray(transformed_image).save(frame_path)
        print(f"Frame {i:04d} gespeichert unter {frame_path} mit Wave Intensity {wave_intensity:.2f}")

# Beispielaufruf
save_frames_with_organic_movement("image.jpg", "output_frames/organic_movement", duration_seconds=10, fps=24, initial_wave_intensity=5, wave_intensity_step=0.1, frequency=0.1)
