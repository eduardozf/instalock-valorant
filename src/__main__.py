import sys
from .macro import InstalockMacro

def main():
    try:
        macro = InstalockMacro()
        macro.start_listening()
    except Exception as e:
        print(f"\n⚠️ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 