import os
from pathlib import Path

from colorama import Fore, Style
from termcolor import colored


class ascii_monet:
    
    def __init__(self):
        ...
    
    @classmethod
    def generate(self, path):
        print('PATH TO IMAGE:', path)
        print(Path(os.curdir).resolve())
        print("TEST IMAGE:")
        print("\033[31mThis is red text\033[0m")
        print("\033[1;31mBold red text\033[0m")
        print("\033[4;34mUnderlined blue text\033[0m")
        print()
