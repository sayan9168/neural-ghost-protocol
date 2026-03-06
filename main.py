import argparse
from core.engine import GhostEngine

def main():
    parser = argparse.ArgumentParser(description="Neural Ghost Protocol: Stealth Data Injection")
    parser.add_argument("--mode", choices=["encode", "decode"], required=True)
    parser.add_argument("--img", help="Input image path", required=True)
    parser.add_argument("--msg", help="Message to hide (only for encode mode)")
    parser.add_argument("--out", help="Output path (default: ghost_out.png)", default="ghost_out.png")

    args = parser.parse_args()
    engine = GhostEngine()

    if args.mode == "encode":
        if not args.msg:
            print("Error: Message is required for encoding.")
            return
        engine.encode(args.img, args.msg, args.out)
        print(f"Successfully injected secret layer into {args.out}")
    
    elif args.mode == "decode":
        result = engine.decode(args.img)
        print(f"Decoded Message: {result}")

if __name__ == "__main__":
    main()
  
