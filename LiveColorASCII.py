# termial color
from PIL import Image
import os
import cv2
import subprocess
import pyautogui


# allow windows to use color in the terminal
os.system("color 0a")



# ascii_characters_by_surface = " `^\",:;Il!i~+_-?tfjrxnuvcz0mwqpdbkhao*#MW&8%B@$"
ascii_characters_by_surface = [' ', '.', "'", ',', '`', ':', '"', '_', ';', '-', '!', 'I', 'i', 'l', '^', 'r', 'v', '1', 'f', 't', 'j', '~', 'h', 'a', 'A', 'k', 'e', 'C', '4', 'w', 'U', '3', 'X', 'b', 'd', 'p', 'q', 'Z', 'P', '2', 'E', 'H', '0', '5', 'G', 'S', 'O', 'g', 'K', '6', '9', 'D', 'm', 'N', '8', 'R', 'Q', 'B', 'W', 'M', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█', '▉', '▊', '▋', '▌', '▍', '▎', '▏', '▐', '░', '▒', '▓', '&', '%', '#', '@', '$'] 


# funct to take a photo using the webcam
def take_photo(show = False):
    capture = cv2.VideoCapture(0)
    ret , frame = capture.read()
    if show:
        cv2.imshow('frame', frame)
        cv2.waitKey(0)
    return frame

def mainConvertor():
    
    imageNumpy = take_photo()
    # how to get the dimensions of the image
    height, width, channels = imageNumpy.shape

    imageNumpy = cv2.resize(imageNumpy, (int(width / 10 * 2.5), int(height / 10)),interpolation=cv2.INTER_AREA)
    width, height = int(width / 10 * 2.5), int(height / 10)

    ascii_art = convert_to_ascii_art(imageNumpy, width, height)

    return ascii_art,imageNumpy

def convert_to_ascii_art(image,width, height):
    ascii_art = []
    for i in range(height):
        line = ''
        for j in range(width):
            line += convert_pixel_to_character(image[i][j])
        ascii_art.append(line)

    return ascii_art


def convert_pixel_to_character(pixel):
    (r, g, b) = pixel
    pixel_brightness = r + g + b
    max_brightness = 255 * 3
    brightness_weight = len(ascii_characters_by_surface) / max_brightness
    index = int(pixel_brightness * brightness_weight) - 1
    return ascii_characters_by_surface[index]


def read_text():
    with open("image.txt", "r") as file:
        text = ''
        for line in file:
            text += line
    return text

def fix_rgb(r,g,b,strong = False,Strongthreshold = 150):
    # checking
    if strong:
        for rgb in [r,g,b]:
            if rgb < Strongthreshold:
                rgb = 0
        for rgb in [r,g,b]:
            if rgb > Strongthreshold:
                rgb = 255
    else:
        for rgb in [r,g,b]:
            if rgb < 100:
                rgb = 0
        for rgb in [r,g,b]:
            if rgb > 200:
                rgb = 255
    return r,g,b
        
def rgb_to_escape(colorlist,text):
    r, g, b = colorlist[0],colorlist[1],colorlist[2]

    r,g,b = fix_rgb(r,g,b)

    print("\033[38;2;{};{};{}m".format(b, g, r) + text + "\033[0m",end='')

if __name__ == "__main__":

    pyautogui.hotkey('super', 'up')
    cap = cv2.VideoCapture(0)
    
    while True and 0XFF != ord('q'):

        ascii,imageValues = mainConvertor()
        
        # clear the terminal
        os.system('cls')

        pixel_x = 0
        pixel_y = 0
        

        for line in ascii:
            pixel_y = 0
            for chara in line:
                rgb_to_escape(imageValues[pixel_x][pixel_y],chara)
                pixel_y += 1
            print()
            pixel_x += 1
        
        




    
