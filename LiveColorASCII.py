# V3
# 11/10/2023
'''
Updates:
    - Dynamic Resizing
    - Fixed the weird buffer issue
    - Cleaned the code
    - Removed Redundant Libraries

TODO:
    - Add Documentation
    - Fix Existing Documentation
    - Add Command Line Arguments for different Modes
'''

import cv2
from os import system
from pyautogui import size
from numpy import array, mean

def TakeFrame(cap):
    """
    -------------------------------------------------------------
    Takes a frame from the camera
    -------------------------------------------------------------
    ### Parameters:
        cap: Camera object [cv2 object]
    ### Returns:
        frame: Frame from the camera [numpy array]
    """
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if not success:
        raise Exception("Could not read Frame")
    return frame

def EndCode(cap):
    """
    -------------------------------------------------------------
    Ends the code
        - Releases the camera
        - Destroys all the windows
    -------------------------------------------------------------
    ### Parameters:
        cap: Camera object [cv2 object]

    """

    if cv2.waitKey(1) == ord("q"):
        cap.release()
        print("Camera Released")
        exit()

def MainConvertor(frame, resize=True, resize_factor = 15, debug=False):
    height, width, _ = frame.shape
    if resize:
        # resize_width, resize_height = int(width / 10 * 2.5), int(height / 10)
        resize_width, resize_height = int(1920 / resize_factor), int(1080 / resize_factor)
        frame = cv2.resize(frame, (resize_width,resize_height), cv2.INTER_LINEAR) 

        # update the height and width
        height, width = resize_height, resize_width

    ascii_art = ConvertToASCII(frame, height, width)

    return ascii_art

def ConvertToASCII(frame,height, width, BW = False, inverted = False):
    ascii_art = []

    if BW:
        for i in range(0, height, 2):
            line = ""
            for j in range(0, width):
                pixel = frame[i, j]
                line += character_list[int(mean(pixel) / 25)]
            ascii_art.append(line)

    elif inverted:
        for i in range(0, height, 2): 
            line = ""
            for j in range(0, width):
                pixel = frame[i, j]
                line += inverted_character_list[int(mean(pixel) / 25)]
            ascii_art.append(line)
    else:
        for i in range(0, height, 2):
            line = ""
            for j in range(0, width):
                pixel = frame[i, j]
                r, g, b = pixel[0],pixel[1],pixel[2]
                # fixing the rgb values
                r,g,b = FixColors(r,g,b)
                line += "\033[38;2;{};{};{}m".format(pixel[2],pixel[1],pixel[0]) + character_list[int(mean(pixel) / 25)] + "\033[0m"
            ascii_art.append(line)


    return ascii_art

def FixColors(r,g,b):
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

    for rgb in [r,g,b]:
        # if the rgb value is less than 100 it will be 0
        if rgb < 150:
            rgb = 0
            # pass
    for rgb in [r,g,b]:
        # if the rgb value is more than 200 it will be 255
        if rgb > 200:
            rgb = 255
    r,g,b = r+50,g+50,b+50
    return r,g,b
    
def PrintArt(ascii_art):
    for line in ascii_art:
        print(line)


def main():
    global screen_width, screen_height
    screen_width, screen_height = size()

    global character_list, inverted_character_list
    # character_list  = " `^\",:;Il!i~+_-?tfjrxnuvcz0mwqpdbkhao*#MW&8%B@$"
    # character_list  = array([' ', '.', '!', 'I', 'i', 'l', '^', 'r', 'v', '1', 'f', 't', 'j', '#', '@', '$'])
    character_list = array([' ', '.', '!', 'I', 'i', 'l', '^', 'r', 'v', '1', 'f', 't', 'j', '#', '@', '$'])
    inverted_character_list = character_list[::-1]


    system("color 0a")

    capture = cv2.VideoCapture(0)
    while capture.isOpened():
        frame = TakeFrame(capture)
        ascii_art = MainConvertor(frame, resize=True, debug=False)
        PrintArt(ascii_art)
        
        # showImage(frame, changeSize=False)  # for testing
        EndCode(capture)  # taken from Sketch-Air.py



if __name__ == "__main__":
    print("Starting...")
    main()

        

