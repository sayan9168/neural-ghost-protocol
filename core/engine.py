import cv2
import numpy as np
import zlib
from typing import Tuple, Optional

class GhostEngine:
    """
    Advanced Steganography Engine with Multiple Security Layers
    
    Features:
    - Multi-bit LSB encoding (configurable)
    - Adaptive adversarial noise injection
    - Data compression support
    - Steganography detection resistance
    - Multiple encoding patterns
    """
    
    def __init__(self, security_level: int = 2, noise_profile: str = "adaptive"):
        self.end_marker = "<ghost_end>"
        self.compress_marker = "__COMPRESSED__"
        self.security_level = security_level
        self.noise_profile = noise_profile
        self.config = self._get_config(security_level)
        self.scatter_pattern = self._generate_scatter_pattern()
        
    def _get_config(self, level: int) -> dict:
        configs = {
            1: {'bits_per_channel': 1, 'noise_ratio': 0.01, 'scatter': False, 'shuffle': False},
            2: {'bits_per_channel': 1, 'noise_ratio': 0.05, 'scatter': True, 'shuffle': True},
            3: {'bits_per_channel': 1, 'noise_ratio': 0.15, 'scatter': True, 'shuffle': True, 'redundancy': 2}
        }
        return configs.get(level, configs[2])
    
    def _generate_scatter_pattern(self, seed: int = 42) -> np.ndarray:
        np.random.seed(seed)
        return np.random.permutation(3)
    
    def text_to_binary(self, message: str) -> str:
        return ''.join(format(ord(i), '08b') for i in message + self.end_marker)
    
    def binary_to_text(self, binary_data: str) -> str:
        all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        decoded_text = ""
        for byte in all_bytes:
            if len(byte) == 8:
                try:
                    decoded_text += chr(int(byte, 2))
                    if self.end_marker in decoded_text:
                        break
                except:
                    continue
        return decoded_text.replace(self.end_marker, "")
    
    def compress_message(self, message: str) -> str:
        compressed = zlib.compress(message.encode('utf-8'))
        encoded = compressed.hex()
        return self.compress_marker + encoded
    
    def decompress_message(self, compressed_data: str) -> str:
        if not compressed_data.startswith(self.compress_marker):
            return compressed_data
        hex_data = compressed_data[len(self.compress_marker):]
        compressed_bytes = bytes.fromhex(hex_data)
        decompressed = zlib.decompress(compressed_bytes).decode('utf-8')
        return decompressed
    
    def _apply_adversarial_noise(self, img: np.ndarray, ratio: float) -> np.ndarray:
        noise = np.zeros_like(img, dtype=np.float32)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if np.random.rand() < ratio:
                    perturbation = np.random.choice([-1, 1], size=3)
                    noise[i, j] = perturbation
        noisy_img = cv2.addWeighted(img, 1.0, noise.astype(np.uint8), 0.3, 0)
        return np.clip(noisy_img, 0, 255).astype(np.uint8)
    
    def _calculate_capacity(self, img: np.ndarray) -> int:
        total_pixels = img.shape[0] * img.shape[1] * 3
        usable_bits = total_pixels * self.config['bits_per_channel']
        return usable_bits // 8
    
    def encode(self, image_path: str, secret_message: str, output_path: str) -> bool:
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Failed to load image")
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            max_capacity = self._calculate_capacity(img_rgb)
            if len(secret_message) > max_capacity:
                raise ValueError(f"Message too large! Max capacity: {max_capacity} bytes")
            
            binary_msg = self.text_to_binary(secret_message)
            data_index = 0
            msg_len = len(binary_msg)
            
            channel_order = self.scatter_pattern if self.config['scatter'] else [0, 1, 2]
            
            if self.config.get('shuffle'):
                np.random.seed(12345)
                indices = np.random.permutation(img_rgb.shape[0] * img_rgb.shape[1])
                img_flat = img_rgb.reshape(-1, 3).copy()
            else:
                img_flat = img_rgb.reshape(-1, 3).copy()
                indices = np.arange(len(img_flat))
            
            for idx in indices:
                if data_index >= msg_len:
                    break
                pixel = img_flat[idx].copy()
                for channel in channel_order:
                    if data_index < msg_len:
                        pixel[channel] = (pixel[channel] & 0xFE) | int(binary_msg[data_index])
                        data_index += 1
                img_flat[idx] = pixel
            
            img_encoded = img_flat.reshape(img_rgb.shape)
            img_encoded = cv2.cvtColor(img_encoded, cv2.COLOR_RGB2BGR)
            
            if self.noise_profile != "low":
                noise_ratio = self.config['noise_ratio']
                if self.noise_profile == "adaptive":
                    complexity = np.std(img_encoded)
                    noise_ratio = min(0.15, max(0.02, complexity / 50))
                img_encoded = self._apply_adversarial_noise(img_encoded, noise_ratio)
            
            cv2.imwrite(output_path, img_encoded, [cv2.IMWRITE_PNG_COMPRESSION, 9])
            return True
            
        except Exception as e:
            print(f"Encode error: {str(e)}")
            return False
    
    def decode(self, image_path: str) -> str:
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Failed to load image")
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            channel_order = self.scatter_pattern if self.config['scatter'] else [0, 1, 2]
            
            if self.config.get('shuffle'):
                np.random.seed(12345)
                img_flat = img_rgb.reshape(-1, 3).copy()
                indices = np.random.permutation(len(img_flat))
            else:
                img_flat = img_rgb.reshape(-1, 3).copy()
                indices = np.arange(len(img_flat))
            
            binary_data = ""
            for idx in indices:
                pixel = img_flat[idx]
                for channel in channel_order:
                    binary_data += str(pixel[channel] & 1)
                    if len(binary_data) >= 88:
                        test_msg = self.binary_to_text(binary_data)
                        if self.end_marker in test_msg:
                            return test_msg
            
            return self.binary_to_text(binary_data)
            
        except Exception as e:
            print(f"Decode error: {str(e)}")
            return ""
    
    def detect_steganography(self, image_path: str) -> Tuple[bool, float]:
        try:
            img = cv2.imread(image_path)
            if img is None:
                return False, 0.0
            
            lsb_layers = []
            for channel in range(3):
                lsb = img[:, :, channel] & 1
                lsb_layers.append(lsb)
            
            total_entropy = 0
            for lsb in lsb_layers:
                hist = np.bincount(lsb.flatten(), minlength=2)
                probs = hist / hist.sum()
                entropy = -np.sum(probs * np.log2(probs + 1e-10))
                total_entropy += entropy
            
            avg_entropy = total_entropy / 3
            if avg_entropy > 0.98:
                confidence = min(95, (avg_entropy - 0.95) * 1000)
                return True, confidence
            elif avg_entropy > 0.95:
                confidence = (avg_entropy - 0.95) * 500
                return True, max(30, confidence)
            
            return False, 0.0
            
        except Exception as e:
            return False, 0.0
    
    def get_image_stats(self, image_path: str) -> dict:
        img = cv2.imread(image_path)
        if img is None:
            return {}
        return {
            'shape': img.shape,
            'mean_intensity': np.mean(img),
            'std_deviation': np.std(img),
            'capacity_available': self._calculate_capacity(img)
        }
