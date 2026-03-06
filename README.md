# Neural Ghost Protocol (NGP)

Neural Ghost Protocol is an advanced **Adversarial Steganography** tool designed for secure data stealth. Unlike traditional cryptography, NGP hides data in plain sight by manipulating image pixels at a granular level and injecting adversarial noise to confuse AI-driven forensic scanners.

## Key Features
- **AI-Resistant Layer:** Injects stochastic noise to bypass neural network-based detection.
- **LSB Encoding:** Efficiently hides payloads within image bitstreams.
- **Fingerprint Locking Ready:** Modular structure allowing integration with biometric authentication.

## Installation
```bash
pip install -r requirements.txt
Usage
To Hide a Message:
python main.py --mode encode --img input.jpg --msg "Secret Data Here" --out secure_output.png
To Retrieve a Message:
python main.py --mode decode --img secure_output.png
Security Disclaimer
This tool is for research and privacy protection purposes only.
