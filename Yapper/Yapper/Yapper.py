import sounddevice as sd
import numpy as np
import keyboard
import time
import threading

# Initialize the threshold and keybinding
THRESHOLD = 50.00
KEY_TO_PRESS = 'z'

stream = None  # Initialize stream to None

def audio_callback(indata, frames, time, status):
    global THRESHOLD, KEY_TO_PRESS
    volume_norm = np.linalg.norm(indata) * 10
    print(f"Volume: {volume_norm:.2f}")
    
    # If the sound is loud enough, press the key
    if volume_norm > THRESHOLD:
        keyboard.press(KEY_TO_PRESS)
    else:
        keyboard.release(KEY_TO_PRESS)

def input_thread():
    global THRESHOLD, KEY_TO_PRESS, stream
    
    while True:
        input("Press Enter to change the threshold and keybinding.")
        
        # Stop the stream
        if stream:
            stream.stop()
            stream.close()

        new_threshold = input("Enter new threshold value: ")
        try:
            THRESHOLD = float(new_threshold)
            print(f"Threshold set to: {THRESHOLD}")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
        
        new_key = input("Enter new key to press: ")
        if len(new_key) == 1:
            KEY_TO_PRESS = new_key
            print(f"Keybinding set to: {KEY_TO_PRESS}")
        else:
            print("Invalid input. Please enter a single key.")
        
        # Restart the stream
        stream = sd.InputStream(callback=audio_callback)
        stream.start()

# Start a thread to handle user input for changing the threshold and keybinding
thread = threading.Thread(target=input_thread, daemon=True)
thread.start()

# Start streaming from the microphone
stream = sd.InputStream(callback=audio_callback)
stream.start()

while True:
    time.sleep(0.1)
