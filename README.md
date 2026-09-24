# Neural Ghost Protocol v2.0 (NGP)

## Advanced Adversarial Steganography System

Neural Ghost Protocol is a state-of-the-art **steganography toolkit** designed for secure data hiding with AI-resistant features. Unlike traditional cryptography that encrypts data, NGP hides data in plain sight within images using advanced LSB (Least Significant Bit) manipulation combined with adversarial noise injection.

## 🚀 New Features in v2.0

### Core Enhancements
- **AES-256 Encryption**: Optional password-based encryption before hiding
- **Data Compression**: zlib compression for larger messages
- **Multi-Level Security**: 3 security levels (Fast, Balanced, Maximum Stealth)
- **Adaptive Noise**: Smart noise injection based on image complexity
- **Batch Processing**: Process multiple images at once
- **Verification Mode**: Verify encoded data integrity
- **Metadata Extraction**: View image statistics and EXIF data
- **Steganography Detection**: Built-in detector to identify hidden data

### Technical Features
- Shuffled pixel encoding for enhanced security
- Channel scattering for distributed data hiding
- Statistical analysis resistance
- AI/ML detector evasion capabilities

## Installation

```bash
pip install -r requirements.txt
```

### Requirements
- Python 3.8+
- numpy >= 1.21.0
- opencv-python >= 4.5.0
- Pillow >= 9.0.0
- cryptography >= 36.0.0

## Usage

### Basic Encoding (No Encryption)
```bash
python main.py --mode encode --img input.jpg --msg "Secret Message" --out output.png
```

### Encoding with AES-256 Encryption
```bash
python main.py --mode encode --img input.jpg --msg "Secret" --pass "mypassword" --out secure.png
```

### Decoding (Without Password)
```bash
python main.py --mode decode --img secure.png
```

### Decoding (With Password)
```bash
python main.py --mode decode --img secure.png --pass "mypassword"
```

### Batch Encoding
```bash
python main.py --mode batch-encode --folder ./images --msg "Hidden Data" --pass "key123" --recursive
```

### Batch Decoding
```bash
python main.py --mode batch-decode --folder ./processed --pass "key123"
```

### Metadata Analysis
```bash
python main.py --mode meta --img image.png
```

### Steganography Detection
```bash
python main.py --mode verify --img suspicious_image.png
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--mode` | Operation mode: encode, decode, batch-encode, batch-decode, meta, verify |
| `--img` | Input image path (single file mode) |
| `--msg` | Message to hide (encode mode only) |
| `--msg-file` | Read message from file (alternative to --msg) |
| `--out` | Output path (default: ghost_out.png) |
| `--pass` | Encryption password (AES-256) |
| `--level` | Security level: 1=Fast, 2=Balanced, 3=Maximum Stealth |
| `--compress` | Compress message before encoding |
| `--verify-out` | Verify output after encoding |
| `--folder` | Folder for batch operations |
| `--pattern` | File pattern for batch mode (default: *.png) |
| `--recursive` | Search recursively in batch mode |
| `--stats` | Show detailed statistics |
| `--noise-profile` | Adversarial noise: low, medium, high, adaptive |

## Security Levels

### Level 1 (Fast)
- Minimal noise injection
- No pixel shuffling
- Best for quick operations

### Level 2 (Balanced) - Default
- Moderate noise injection
- Pixel shuffling enabled
- Channel scattering
- Good balance of speed and security

### Level 3 (Maximum Stealth)
- High noise injection
- Full pixel shuffling
- Channel scattering
- Redundancy encoding
- Maximum resistance to detection

## How It Works

1. **Message Processing**: Optional encryption and compression
2. **Binary Conversion**: Text converted to binary stream
3. **Pixel Selection**: Shuffled/random pixel selection (Level 2+)
4. **LSB Modification**: Hide bits in least significant bits
5. **Noise Injection**: Add adversarial perturbations
6. **Output**: Save as PNG with lossless compression

## Examples

### Hide a Long Message with All Features
```bash
python main.py --mode encode \
  --img photo.jpg \
  --msg "This is a very long secret message that needs maximum protection!" \
  --pass "StrongPassword123!" \
  --level 3 \
  --compress \
  --verify-out \
  --stats \
  --out protected.png
```

### Scan a Folder for Hidden Messages
```bash
python main.py --mode batch-decode \
  --folder /path/to/images \
  --pass "password" \
  --recursive \
  --pattern "*.jpg"
```

## ⚠️ Disclaimer

This tool is provided for **research and educational purposes only**. The authors are not responsible for any misuse of this software. Always ensure you have permission to modify images and comply with local laws regarding data privacy and security.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please submit pull requests or open issues for bugs and feature requests.
