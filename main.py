import argparse
import sys
from core.engine import GhostEngine
from core.crypto import CryptoLayer
from core.utils import ImageValidator, MetadataHandler

def main():
    parser = argparse.ArgumentParser(
        description="Neural Ghost Protocol v2.0: Advanced Stealth Data Injection System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic encoding with encryption
  python main.py --mode encode --img input.jpg --msg "Secret" --pass "mypassword" --out secure.png
  
  # Decode with password
  python main.py --mode decode --img secure.png --pass "mypassword"
  
  # Batch processing
  python main.py --mode batch-encode --folder ./images --msg "Data" --pass "key123"
  
  # Extract metadata
  python main.py --mode meta --img secure.png
        """
    )
    
    parser.add_argument("--mode", choices=["encode", "decode", "batch-encode", "batch-decode", "meta", "verify"], 
                       required=True, help="Operation mode")
    parser.add_argument("--img", help="Input image path (single file mode)")
    parser.add_argument("--msg", help="Message to hide (encode mode only)")
    parser.add_argument("--msg-file", help="Read message from file (alternative to --msg)")
    parser.add_argument("--out", help="Output path (default: ghost_out.png)", default="ghost_out.png")
    parser.add_argument("--pass", dest="password", help="Encryption password (AES-256)")
    parser.add_argument("--level", type=int, choices=[1, 2, 3], default=2, 
                       help="Security level: 1=Fast, 2=Balanced, 3=Maximum Stealth")
    parser.add_argument("--compress", action="store_true", help="Compress message before encoding")
    parser.add_argument("--verify-out", action="store_true", help="Verify output after encoding")
    parser.add_argument("--folder", help="Folder for batch operations")
    parser.add_argument("--pattern", default="*.png", help="File pattern for batch mode")
    parser.add_argument("--recursive", action="store_true", help="Search recursively in batch mode")
    parser.add_argument("--stats", action="store_true", help="Show detailed statistics")
    parser.add_argument("--noise-profile", choices=["low", "medium", "high", "adaptive"], 
                       default="adaptive", help="Adversarial noise intensity")

    args = parser.parse_args()
    
    # Initialize components
    engine = GhostEngine(security_level=args.level, noise_profile=args.noise_profile)
    crypto = CryptoLayer() if args.password else None
    
    try:
        if args.mode == "encode":
            handle_encode(args, engine, crypto)
        elif args.mode == "decode":
            handle_decode(args, engine, crypto)
        elif args.mode == "batch-encode":
            handle_batch_encode(args, engine, crypto)
        elif args.mode == "batch-decode":
            handle_batch_decode(args, engine, crypto)
        elif args.mode == "meta":
            handle_metadata(args)
        elif args.mode == "verify":
            handle_verify(args, engine)
            
    except Exception as e:
        print(f"\n[ERROR] Operation failed: {str(e)}", file=sys.stderr)
        if args.stats:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def handle_encode(args, engine, crypto):
    """Handle single file encoding with optional encryption"""
    if not args.msg and not args.msg_file:
        print("[ERROR] Message required (--msg or --msg-file)", file=sys.stderr)
        sys.exit(1)
    
    # Get message
    message = args.msg
    if args.msg_file:
        with open(args.msg_file, 'r', encoding='utf-8') as f:
            message = f.read()
    
    # Validate input image
    validator = ImageValidator(args.img)
    if not validator.validate():
        print(f"[ERROR] Invalid image: {validator.error}", file=sys.stderr)
        sys.exit(1)
    
    # Encrypt if password provided
    if crypto:
        print(f"[*] Encrypting message with AES-256...")
        message = crypto.encrypt(message, args.password)
        print(f"[OK] Encryption complete")
    
    # Compress if requested
    if args.compress and len(message) > 100:
        print(f"[*] Compressing message...")
        message = engine.compress_message(message)
        print(f"[OK] Compression complete ({len(message)} bytes)")
    
    # Encode
    print(f"[*] Injecting data into {args.img}...")
    success = engine.encode(args.img, message, args.out)
    
    if success:
        print(f"[OK] Successfully injected secret layer into {args.out}")
        
        # Verify if requested
        if args.verify_out:
            print(f"[*] Verifying output...")
            decoded = engine.decode(args.out)
            if crypto:
                decoded = crypto.decrypt(decoded, args.password)
            if decoded == message:
                print(f"[OK] Verification successful - data integrity confirmed")
            else:
                print(f"[WARNING] Verification mismatch!", file=sys.stderr)
        
        # Show stats
        if args.stats:
            meta = MetadataHandler(args.out)
            stats = meta.get_statistics()
            print(f"\n=== Output Statistics ===")
            print(f"File size: {stats['size']} bytes")
            print(f"Dimensions: {stats['dimensions']}")
            print(f"Format: {stats['format']}")
            print(f"Capacity used: {stats['capacity_used']:.2f}%")
    else:
        print(f"[ERROR] Encoding failed", file=sys.stderr)
        sys.exit(1)


def handle_decode(args, engine, crypto):
    """Handle single file decoding with optional decryption"""
    if not args.img:
        print("[ERROR] Input image required (--img)", file=sys.stderr)
        sys.exit(1)
    
    print(f"[*] Extracting hidden data from {args.img}...")
    result = engine.decode(args.img)
    
    # Decompress if needed (auto-detect)
    if result.startswith("__COMPRESSED__"):
        print(f"[*] Detected compressed data, decompressing...")
        result = engine.decompress_message(result)
    
    # Decrypt if password provided
    if crypto:
        print(f"[*] Decrypting message...")
        try:
            result = crypto.decrypt(result, args.password)
            print(f"[OK] Decryption successful")
        except Exception as e:
            print(f"[ERROR] Decryption failed - wrong password?", file=sys.stderr)
            sys.exit(1)
    
    print(f"\n{'='*50}")
    print(f"DECODED MESSAGE:")
    print(f"{'='*50}")
    print(result)
    print(f"{'='*50}")


def handle_batch_encode(args, engine, crypto):
    """Handle batch encoding operations"""
    import glob
    import os
    
    if not args.folder:
        print("[ERROR] Folder required for batch mode (--folder)", file=sys.stderr)
        sys.exit(1)
    
    if not args.msg and not args.msg_file:
        print("[ERROR] Message required for batch encoding", file=sys.stderr)
        sys.exit(1)
    
    # Get message
    message = args.msg
    if args.msg_file:
        with open(args.msg_file, 'r', encoding='utf-8') as f:
            message = f.read()
    
    # Find files
    pattern = os.path.join(args.folder, "**", args.pattern) if args.recursive \
              else os.path.join(args.folder, args.pattern)
    files = glob.glob(pattern, recursive=args.recursive)
    
    if not files:
        print(f"[WARNING] No files found matching {pattern}")
        return
    
    print(f"[*] Found {len(files)} files to process")
    
    success_count = 0
    fail_count = 0
    
    for i, img_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {img_path}")
        
        try:
            out_path = os.path.splitext(img_path)[0] + "_ghost.png"
            
            # Encrypt per file if password
            proc_msg = message
            if crypto:
                proc_msg = crypto.encrypt(f"{os.path.basename(img_path)}:{message}", args.password)
            
            if engine.encode(img_path, proc_msg, out_path):
                print(f"[OK] Success -> {out_path}")
                success_count += 1
            else:
                print(f"[FAIL] Encoding failed")
                fail_count += 1
                
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            fail_count += 1
    
    print(f"\n{'='*50}")
    print(f"Batch Complete: {success_count} succeeded, {fail_count} failed")
    print(f"{'='*50}")


def handle_batch_decode(args, engine, crypto):
    """Handle batch decoding operations"""
    import glob
    import os
    
    if not args.folder:
        print("[ERROR] Folder required for batch mode (--folder)", file=sys.stderr)
        sys.exit(1)
    
    pattern = os.path.join(args.folder, "**", args.pattern) if args.recursive \
              else os.path.join(args.folder, args.pattern)
    files = glob.glob(pattern, recursive=args.recursive)
    
    if not files:
        print(f"[WARNING] No files found matching {pattern}")
        return
    
    print(f"[*] Scanning {len(files)} files for hidden data...")
    
    results = []
    for i, img_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Scanning: {img_path}")
        
        try:
            result = engine.decode(img_path)
            
            if result and len(result) > 10:  # Filter noise
                if crypto:
                    try:
                        result = crypto.decrypt(result, args.password)
                    except:
                        continue  # Skip if decryption fails
                
                results.append((img_path, result))
                print(f"[FOUND] Hidden data detected!")
            else:
                print(f"[NONE] No hidden data found")
                
        except Exception as e:
            print(f"[ERROR] {str(e)}")
    
    if results:
        print(f"\n{'='*50}")
        print(f"BATCH DECODE RESULTS ({len(results)} files with data):")
        print(f"{'='*50}")
        for path, msg in results:
            print(f"\nFile: {path}")
            print(f"Message: {msg[:100]}{'...' if len(msg) > 100 else ''}")
    else:
        print(f"\n[INFO] No hidden data found in any files")


def handle_metadata(args):
    """Extract and display image metadata"""
    if not args.img:
        print("[ERROR] Image path required (--img)", file=sys.stderr)
        sys.exit(1)
    
    meta = MetadataHandler(args.img)
    stats = meta.get_statistics()
    exif = meta.extract_exif()
    
    print(f"\n{'='*50}")
    print(f"METADATA REPORT: {args.img}")
    print(f"{'='*50}")
    print(f"File Size: {stats['size']} bytes")
    print(f"Dimensions: {stats['dimensions']}")
    print(f"Format: {stats['format']}")
    print(f"Color Mode: {stats['color_mode']}")
    print(f"Capacity Used: {stats['capacity_used']:.2f}%")
    
    if exif:
        print(f"\n--- EXIF Data ---")
        for key, value in exif.items():
            print(f"{key}: {value}")
    else:
        print(f"\n[INFO] No EXIF data found")
    
    print(f"{'='*50}")


def handle_verify(args, engine):
    """Verify steganographic integrity"""
    if not args.img:
        print("[ERROR] Image path required (--img)", file=sys.stderr)
        sys.exit(1)
    
    print(f"[*] Analyzing {args.img} for steganographic markers...")
    
    is_modified, confidence = engine.detect_steganography(args.img)
    
    print(f"\n{'='*50}")
    print(f"STEGANOGRAPHY DETECTION REPORT")
    print(f"{'='*50}")
    print(f"Modified: {'YES' if is_modified else 'NO'}")
    print(f"Confidence: {confidence:.1f}%")
    
    if is_modified and confidence > 80:
        print(f"[ALERT] High probability of hidden data detected!")
    elif is_modified:
        print(f"[INFO] Possible modifications detected")
    else:
        print(f"[OK] No steganographic signatures detected")
    
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
