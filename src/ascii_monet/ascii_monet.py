import os
import shutil
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from colorama import just_fix_windows_console, init
just_fix_windows_console() # gets ANSI working in Windows CMD
# init(strip=False) 

class ascii_monet:
    
    fonts = [
        "assets/Anonymous.ttf",
        "assets/fonts/iAWriterDuospace-Regular.otf",
        "assets/fonts/CascadiaMono-Regular.otf",
    ]
    font_path = os.path.join(os.path.dirname(__file__), fonts[-1])
    
    
    @classmethod
    def generate(cls, path, custom_chars=None, only_alphanum=False, only_alpha=False, terminal_width=False, height=None, width=80, max_height=100, max_width=None):
        """ Given a path to an image, generates colored ASCII art of the image in the terminal """

        image_path = os.path.join(os.curdir, path)
        if not os.path.exists(image_path):
            print('ERROR: Path does not exist: "{}"'.format(image_path))
            return 1
        
        print('Generating ASCII art of image: "{}"'.format(image_path))
        # print("\033[38;2;0;0;0mThis should be black text\033[0m")
        
        chars = cls.getCharsToUse(custom_chars=custom_chars, only_alphanum=only_alphanum, only_alpha=only_alpha)
        # print(chars)
        
        image = np.array(Image.open(image_path))
        block_size = cls.getBlockSize(image.shape, terminal_width, height, width, max_height, max_width)
        blocks = cls.toBlocks(image, block_size)

        # get average block pixel values
        colors = []
        for row in blocks:
            for char in row:
                pixel_mean = np.astype(np.mean(char, axis=(0, 1)), np.uint8)
                char = cls.getChar(pixel_mean, chars)
                cls.print_colored_text(char, pixel_mean, end='')
            print()

    
    @classmethod
    def print_colored_text(cls, text, RGB, bold=True, end=None):
        fmt = "\033[{};38;2;{};{};{}m{}\033[0m"
        cls.print_ansi(text, RGB, bold=True, end=end)
    
    @staticmethod
    def print_ansi(text, RGB, bold=True, end=None):
        bold_bit = '1' if bold else '0'
        fmt = "\033[{};38;2;{};{};{}m{}\033[0m"
        string = fmt.format(bold_bit, *RGB, text)
        print(string, end=end)
    
    
    @staticmethod
    def toBlocks(img, block_size=(8, 8)):
        block_rows, block_cols = block_size
        hei = math.floor( img.shape[0]/block_rows )
        wid = math.floor( img.shape[1]/block_cols )
        depth = math.floor( img.shape[2] )
        blocks = np.empty((hei, wid, block_rows, block_cols, depth), dtype=np.uint8)
        for J in range(hei):
            for I in range(wid):
                block = img[
                    J*block_rows:(J+1)*block_rows,
                    I*block_cols:(I+1)*block_cols,
                ]
                blocks[J][I] = block
        return blocks
    
    @classmethod
    def getChar(cls, px_mean, chars):
        luminance = np.mean(px_mean)
        idx = math.floor(cls.map_value(luminance, 0, 255, 0, len(chars)-1))
        return chars[idx]
    

    @classmethod
    def getCharsToUse(cls, custom_chars=None, only_alphanum=False, only_alpha=False):
        chars_upper = [ chr(x) for x in range(65, 91) ]
        chars_lower = [ chr(x) for x in range(97, 123) ]
        chars_digits = [ str(x) for x in range(10) ]
        chars_all = [ chr(x) for x in range(33, 127) ]

        chars = chars_all
        if custom_chars:
            chars = custom_chars
        elif only_alphanum:
            chars = chars_upper + chars_lower + chars_digits
        elif only_alpha:
            chars = chars_upper + chars_lower
        chars.sort(key=lambda ch: cls.get_on_off_pixel_ratio(ch, cls.font_path))
        return chars
    
    @classmethod
    def getBlockSize(cls, img_shape, terminal_width, height, width, max_height, max_width):
        block_size_default = (20,9)
        terminal_height, terminal_width = shutil.get_terminal_size()

        mult = 2
        
        return np.astype(np.array(block_size_default)*mult, int)
    
    #region ###########################  STATIC METHODS #####################  
    
    @staticmethod
    def map_value(x, a_min, a_max, b_min, b_max):
        return b_min + (x - a_min) * (b_max - b_min) / (a_max - a_min)
    
    
    @staticmethod
    def get_on_off_pixel_ratio(char, font_path):
        font_size = 24
        
        ar = 7/12
        img = Image.new('1', (int(font_size*ar), font_size), 0) # '1' mode is 1-bit pixels
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(font_path, font_size)
        draw.text((0, 0), char, font=font, fill=1)

        pixels = list(img.getdata())
        on_pixels = pixels.count(1)
        off_pixels = pixels.count(0)

        total_pixels = on_pixels + off_pixels
        if total_pixels == 0:
            return 0
        return on_pixels / total_pixels
    
    #endregion ###########################  END STATIC METHODS #############  