import cv2
import numpy as np

class GhostEngine:
    def __init__(self):
        self.end_marker = "<ghost_end>"

    def text_to_binary(self, message):
        return ''.join(format(ord(i), '08b') for i in message + self.end_marker)

    def binary_to_text(self, binary_data):
        all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        decoded_text = ""
        for byte in all_bytes:
            decoded_text += chr(int(byte, 2))
            if self.end_marker in decoded_text:
                break
        return decoded_text.replace(self.end_marker, "")

    def encode(self, image_path, secret_message, output_path):
        img = cv2.imread(image_path)
        binary_msg = self.text_to_binary(secret_message)
        
        data_index = 0
        msg_len = len(binary_msg)
        
        # Apply LSB Steganography with Adversarial Noise
        for row in img:
            for pixel in row:
                for channel in range(3):
                    if data_index < msg_len:
                        pixel[channel] = int(format(pixel[channel], '08b')[:-1] + binary_msg[data_index], 2)
                        data_index += 1
                    else:
                        # Adversarial Noise Layer
                        if np.random.rand() > 0.99:
                            pixel[channel] = (pixel[channel] + 1) % 256
            if data_index >= msg_len:
                break
        
        cv2.imwrite(output_path, img)
        return True

    def decode(self, image_path):
        img = cv2.imread(image_path)
        binary_data = ""
        for row in img:
            for pixel in row:
                for channel in range(3):
                    binary_data += format(pixel[channel], '08b')[-1]
        
        return self.binary_to_text(binary_data)
                  
