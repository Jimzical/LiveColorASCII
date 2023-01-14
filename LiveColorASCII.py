# termial color
from PIL import Image
import os
import cv2
import subprocess
import pyautogui
import sys


# allow windows to use color in the terminal
os.system("color 0a")

# funct to take a photo using the webcam
def take_photo(show = False):
    '''
    ------------------------------------------------
       Take a photo using the webcam               
    ------------------------------------------------
    @param show: if true the photo will be shown   

    @return: the photo as a numpy array
    '''
    capture = cv2.VideoCapture(0)
    ret , frame = capture.read()
    if show:
        cv2.imshow('frame', frame)
        cv2.waitKey(0)
    return frame

def mainConvertor(BW = False):
    '''
    ------------------------------------------------
       Convert the photo to ascii art              
    ------------------------------------------------
    @param BW: if true the photo will be converted to black and white [Default: False]
    
    @return: the ascii art (text) and the image values (for the colors)
    '''
    # take the photo
    imageNumpy = take_photo()

    #  get the dimensions of the image
    height, width, channels = imageNumpy.shape

    # resize the image
    imageNumpy = cv2.resize(imageNumpy, (int(width / 10 * 2.5), int(height / 10)),interpolation=cv2.INTER_AREA)
    # update the dimensions of the image
    width, height = int(width / 10 * 2.5), int(height / 10)

    # convert the image to ascii art
    ascii_art = convert_to_ascii_art(imageNumpy, width, height, BW)

    return ascii_art,imageNumpy

def convert_to_ascii_art(image,width, height, BW = False):
    '''
    ------------------------------------------------
       Convert the photo to ascii art              
    ------------------------------------------------
    @param image: the image as a numpy array
    @param width: the width of the image
    @param height: the height of the image
    @param BW: if true the photo will be converted to black and white [Default: False]

    @return: the ascii art (text)
    '''
    ascii_art = []
    for i in range(height):
        line = ''
        for j in range(width):
            # convert the pixel to a character
            line += convert_pixel_to_character(image[i][j],BW)
        ascii_art.append(line)

    return ascii_art


def convert_pixel_to_character(pixel,BW = False,background = False):
    '''
    ------------------------------------------------
      Convert the pixel to a character            
    ------------------------------------------------
    @param pixel: the pixel as a list of 3 numbers (r,g,b)
    @param BW: if true the photo will be converted to black and white [Default: False]
    @param background: if true the background will be black [Default: False]

    @return: the character
    '''

    # setting the ascii characters by surface area
    ascii_characters_by_surface_BW = " `^\",:;Il!i~+_-?tfjrxnuvcz0mwqpdbkhao*#MW&8%B@$"
    ascii_characters_by_surface = [' ', '.', "'", ',', '`', ':', '"', '_', ';', '-', '!', 'I', 'i', 'l', '^', 'r', 'v', '1', 'f', 't', 'j', '~', 'h', 'a', 'A', 'k', 'e', 'C', '4', 'w', 'U', '3', 'X', 'b', 'd', 'p', 'q', 'Z', 'P', '2', 'E', 'H', '0', '5', 'G', 'S', 'O', 'g', 'K', '6', '9', 'D', 'm', 'N', '8', 'R', 'Q', 'B', 'W', 'M', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█', '▉', '▊', '▋', '▌', '▍', '▎', '▏', '▐', '░', '▒', '▓', '&', '%', '#', '@', '$'] 


    (r, g, b) = pixel
    pixel_brightness = r + g + b
    max_brightness = 255 * 3
    
    if BW:
        ascii_characters_by_surface = ascii_characters_by_surface_BW
    if background:
        ascii_characters_by_surface = ascii_characters_by_surface[::-1]
    brightness_weight = len(ascii_characters_by_surface) / max_brightness
    index = int(pixel_brightness * brightness_weight) - 1
    return ascii_characters_by_surface[index]

def fix_rgb(r,g,b,strong = False,Strongthreshold = 150):
    '''
    -------------------------------------------------------------------------------
        Fix the rgb values to be between 0 and 255 and Increase the contrast
        Also if strong is true it will make the rgb values more Saturated
    -------------------------------------------------------------------------------
    @param r: the red value
    @param g: the green value
    @param b: the blue value
    @param strong: if true it will make the rgb values more Saturated [Default: False]
    @param Strongthreshold: the threshold for the strong [Default: 150]

    @return: the fixed rgb values
    '''
    # checking
    if strong:
        for rgb in [r,g,b]:
            if rgb < Strongthreshold:
                # if the rgb value is less than threshold it will be 0
                rgb = 0
        for rgb in [r,g,b]:
            if rgb > Strongthreshold:
                # if the rgb value is more than threshold it will be 255
                rgb = 255
    else:
        for rgb in [r,g,b]:
            # if the rgb value is less than 100 it will be 0
            if rgb < 100:
                rgb = 0
        for rgb in [r,g,b]:
            # if the rgb value is more than 200 it will be 255
            if rgb > 200:
                rgb = 255
    return r,g,b
        
def rgb_to_escape(colorlist,text,background = False):
    '''
    ------------------------------------------------
         Convert the rgb values to an escape sequence so add color to the text
    ------------------------------------------------
    @param colorlist: the rgb values as a list
    @param text: the text to add color to
    @param background: if true the background will be black [Default: False ]

    @return: the text with color
    '''
    # getting the rgb values
    r, g, b = colorlist[0],colorlist[1],colorlist[2]
    # fixing the rgb values
    r,g,b = fix_rgb(r,g,b)
    if background:
        # printing the text with background color
        print("\033[47;30m" + text + "\033[0m",end='')
        # q: can i change the text color here to blue?
        # a: yes you can
        #
    else:
        # printing the text with black color and white background
        print("\033[38;2;{};{};{}m".format(b,g,r) + text + "\033[0m",end='')
if __name__ == "__main__":
    # setting the ascii characters by surface area

    # if the user wants Black and White make it BW = True
    BW = False

    # making it full screen
    pyautogui.hotkey('super', 'up')
    
    while True and 0XFF != ord('q'):
        # get the ascii art and the image values (for the colors)
        ascii,imageValues = mainConvertor(BW = BW)
        
        # clear the terminal
        os.system('cls')


        pixel_x = 0     # for row counti
        pixel_y = 0     # for element index in the row
        
        if BW:
            for line in ascii:
                pixel_y = 0
                for chara in line:
                    # [255,255,255] is white
                    rgb_to_escape([255,255,255],chara)
                    pixel_y += 1
                print()
                pixel_x += 1

        else:
            for line in ascii:
                pixel_y = 0
                for chara in line:
                    # imageValues[pixel_x][pixel_y] is the rgb value of the pixel, chara is the character
                    rgb_to_escape(imageValues[pixel_x][pixel_y],chara)
                    pixel_y += 1
                print()
                pixel_x += 1
        
        




    
