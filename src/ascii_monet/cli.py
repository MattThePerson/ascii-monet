import argparse
from pathlib import Path
from ascii_monet.ascii_monet import ascii_monet

def main():
    parser = argparse.ArgumentParser(
        description="Generate ASCII art from an image."
    )
    parser.add_argument("image_path", nargs="?", help="Path to the image file")
    parser.add_argument('--grayscale', '-g', action='store_true', help='Prints image in grayscale')
    # parser.add_argument('--background-color', '-bc', help='')
    parser.add_argument('--white-background', action='store_true', help='Assumes white background when selecting chars')
    parser.add_argument('--terminal-width', action='store_true', help='')
    parser.add_argument('--terminal-height', action='store_true', help='')
    parser.add_argument('--width', help='', type=int)
    parser.add_argument('--height', help='', type=int)
    parser.add_argument('--max-width', help='', type=int)
    parser.add_argument('--max-height', help='', type=int)
    parser.add_argument('--char-aspect-ratio', help='Aspect ratio of chars given as a string as "H:W"')
    parser.add_argument('--chars-to-use', help='Give a list of chars to use in the image as a string')
    parser.add_argument('--only-alpha-numeric', action='store_true', help='Only use alpha-numeric characters')
    parser.add_argument('--only-alpha', action='store_true', help='Only use alphabetic characters')

    args = parser.parse_args()

    if not args.image_path:
        print("Usage: ascii-monet <image-path> <OPTIONS>")
        exit(1)

    chars_to_use = None if not args.chars_to_use else list(args.chars_to_use)

    print()
    ret = ascii_monet.generate(args.image_path, custom_chars=chars_to_use, only_alphanum=args.only_alpha_numeric, only_alpha=args.only_alpha)
    print()
    exit(ret)


if __name__ == "__main__":
    main()
