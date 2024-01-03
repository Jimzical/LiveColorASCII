# V3.0.1
# 03/01/2024
'''
Updates:
    - Added Documentation
    - Fixed Existing Documentation

Future Updates:
    - Add Command Line Arguments for different Modes
    - Add Screenshot Feature
'''

import cv2
from pyautogui import size
import numpy as np
from numpy import array, mean

def TakeFrame(cap: cv2.VideoCapture) -> np.array:
    '''
    Takes a frame from the camera.

    Parameters
    ----------
    cap : cv2.VideoCapture
        Camera object.

    Returns
    -------
    array
        Frame from the camera as a numpy array.

    Raises
    ------
    Exception
        If the frame cannot be read.

    Example
    -------
    >>> import cv2
    >>> cap = cv2.VideoCapture(0)
    >>> frame = TakeFrame(cap)
    '''
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if not success:
        raise Exception("Could not read Frame")
    return frame

def ImageBlur(img : np.array, sigma : float=1.3) -> np.array:
    '''
    Blurs an image.

    Parameters
    ----------
    img : numpy.ndarray
        The image to be blurred.
    sigma : float, optional
        The value of the blur (default = 1.3) (Range[0-5]).

    Returns
    -------
    numpy.ndarray
        The blurred image.

    Example
    -------
    >>> import cv2
    >>> img = cv2.imread('image.jpg')
    >>> blurred_img = ImageBlur(img)
    '''
    img = cv2.GaussianBlur(img, (0, 0), sigma)  
    img = cv2.addWeighted(img, 1.5, img, -0.5, 0)
    return img

def ChangeBrightness(img : np.array, value : int =30) -> np.array:
    '''
    Changes the brightness of an image.

    Parameters
    ----------
    img : numpy.ndarray
        The image to change the brightness of.
    value : int, optional
        The value of the brightness (default = 30) (Range[0-255]).

    Returns
    -------
    numpy.ndarray
        The image with the brightness changed.

    Example
    -------
    >>> import cv2
    >>> img = cv2.imread('image.jpg')
    >>> brightened_img = ChangeBrightness(img)
    '''
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return img

def showImg(img : np.array, windowName : str ='Image', waitTime : int =0) -> None:
    '''
    Shows an image.

    Parameters
    ----------
    img : numpy.ndarray
        The image to show.
    windowName : str, optional
        The name of the window that will show the image (default = 'Image').
    waitTime : int, optional
        The time that the image will be shown (default = 0 which is forever).

    Example
    -------
    >>> import cv2
    >>> img = cv2.imread('image.jpg')
    >>> showImg(img)
    '''
    cv2.imshow(windowName, img)
    if cv2.waitKey(waitTime) == ord("q"):
        cv2.destroyAllWindows()

def EndCode() -> None:
    '''
    Ends the code by releasing the camera and destroying all the windows.

    Example
    -------
    >>> EndCode()
    '''
    cv2.destroyAllWindows()
    print("Camera Released")
    exit()

def FrameToASCII(frame : np.array, resize : bool =True, resize_factor : int =15) -> str:
    '''
    Converts a frame to ASCII art.

    Parameters
    ----------
    frame : numpy.ndarray
        The input frame to be converted to ASCII art.
    resize : bool, optional
        Flag to indicate whether the frame should be resized, by default True.
    resize_factor : int, optional
        The factor by which the frame should be resized, by default 15.

    Returns
    -------
    str
        The ASCII art representation of the input frame.

    Example
    -------
    >>> import cv2
    >>> frame = cv2.imread('image.jpg')
    >>> ascii_art = FrameToASCII(frame)
    '''
    height, width, _ = frame.shape
    if resize:
        resize_width, resize_height = int(1920 / resize_factor), int(1080 / resize_factor)
        frame = cv2.resize(frame, (resize_width, resize_height), cv2.INTER_LINEAR) 

        # update the height and width
        height, width = resize_height, resize_width

    ascii_art = convertToASCII(frame, height, width)

    return ascii_art

def convertToASCII(frame : np.array, height : int, width : int) -> list:
    '''
    Converts a frame to ASCII art.

    Parameters
    ----------
    frame : numpy.ndarray
        The input frame to be converted to ASCII art.
    height : int
        The height of the frame.
    width : int
        The width of the frame.

    Returns
    -------
    list
        The ASCII art representation of the input frame as a list of strings.

    Example
    -------
    >>> import cv2
    >>> frame = cv2.imread('image.jpg')
    >>> height, width, _ = frame.shape
    >>> ascii_art = convertToASCII(frame, height, width)
    '''
    ascii_art = []

    if BW:
        for i in range(0, height, 2):
            line = ""
            for j in range(0, width):
                pixel = frame[i, j]
                line += character_list[int(mean(pixel) / 25)]
            ascii_art.append(line)

    else:
        for i in range(0, height, 2):
            line = ""
            for j in range(0, width):
                pixel = frame[i, j]
                r, g, b = pixel[0], pixel[1], pixel[2]
                r, g, b = fixColors(r, g, b)
                line += "\033[38;2;{};{};{}m".format(pixel[2], pixel[1], pixel[0]) + character_list[int(mean(pixel) / 25)] + "\033[0m"
            ascii_art.append(line)

    return ascii_art

def fixColors(r : int, g : int, b : int) -> tuple:
    '''
    Fixes the RGB values to be between 0 and 255 and increases the contrast.

    Parameters
    ----------
    r : int
        The red value.
    g : int
        The green value.
    b : int
        The blue value.

    Returns
    -------
    tuple(int, int, int)
        The fixed RGB values.

    Example
    -------
    >>> r, g, b = fixColors(100, 150, 200)
    '''
    for rgb in [r, g, b]:
        if rgb < 150:
            rgb -= 50
    for rgb in [r, g, b]:
        if rgb > 200:
            rgb = 255
    r, g, b = r + 50, g + 50, b + 50
    return r, g, b

def printArt(ascii_art : list) -> None:
    '''
    Prints the ASCII art.

    Parameters
    ----------
    ascii_art : list
        The ASCII art representation of the frame.

    Example
    -------
    >>> ascii_art = ['..##..', '#####.', '######']
    >>> printArt(ascii_art)
    '''
    for line in ascii_art:
        print(line, flush=True)

def main():
    global screen_width, screen_height
    screen_width, screen_height = size()

    global character_list
    character_list = array([' ', '.', '!', 'I', 'i', 'l', '^', 'r', 'v', '1', 'f', 't', 'j', '#', '@', '$'])

    global BW
    BW = False

    inverted = False
    if inverted:
        character_list = character_list[::-1]

    print("Starting Camera...")
    capture = cv2.VideoCapture(0)
    print("Starting Camera...Done")

    while capture.isOpened():
        frame = TakeFrame(capture)
        
        ascii_art = FrameToASCII(frame, resize=True)
        printArt(ascii_art)
        
        EndCode(capture)

if __name__ == "__main__":
    main()