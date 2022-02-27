import numpy as np
import cv2 as cv
import pyautogui as auto
import random

# ----
# So what is really going on here ?
# Well we are using pyAutoGUI to make all the work here.
# However we are also pulling in functionality from OpenCV
# in the form of confidence calculation and image manipulation.
# ----

# Lets load an image template that we want to match from
# Remember to get this a close to what it really is you want to match
# for best results
imageTemplate = cv.imread("./image-templates/test-game-button.png", 0)

# Let's just make a endless loop, we brave!
while(1):

    # Quick info on pyAutoGUI
    # auto.keyDown('<key>')
    # auto.moveTo(100, 200)
    # auto.click()
    #
    # Mouse manipulation: https://pyautogui.readthedocs.io/en/latest/mouse.html
    # Keyboard manipulation: https://pyautogui.readthedocs.io/en/latest/keyboard.html

    # Quick info on why we do random
    # I have included the random line for when you encouter apps/games etc
    # that will try to catch automation. Also sometimes it just pays of to
    # act more like a real human and clicks are slow ...
    #
    # Example here we are pressing the Keyboard key "a"
    # Then sleeping between 50 and 100ms
    #
    # auto.keyDown('a')
    # time.sleep( random.uniform( 0.05, 0.1 )) # Sleep 50ms to 100ms random
    

    # Screen capture
    # Please note that this process takes around 100-150ms so calculate this
    # into your overall manipulation etc. Also we use OpenCV to manipulate the
    # image on the fly (making it grayscaled etc)
    image = auto.screenshot()
    image = cv.cvtColor(np.array(image), 0)
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Let's do the real OpenCV magic here, please note that pyautogui actually
    # have this support build int, but i opt to use OpenCV directly so we can
    # tinker with all the fancy stuff directly.
    #
    # Read more on object detection / matching algorithms
    # https://docs.opencv.org/4.x/df/dfb/group__imgproc__object.html
    matchResolution = cv.matchTemplate(image, imageTemplate, cv.TM_CCOEFF_NORMED)

    # This is where we can tweak a little to messure threshold/confidence in
    # if we found a match on the screen. A place betwen 0.5 and 0.9 is usually
    # very spot on and all you need.
    foundOnScreen = np.where( matchResolution >= 0.7)

    # This will give you the bounding box values of the actual match
    # on the screen capture and the confidence/threshole number
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(matchResolution)
    print("Result: ",min_val, max_val, min_loc, max_loc)

    # Lets use this to play our mini game!
    # Since we already know the button is 100px x 100px then we just
    # need the boundaries minus/plus 50px to center the courser on the button!
    #
    # Just play around until you get the desired result where you can click with
    # your mouse or press a key to get the outcome you are looking for
    #
    # Also from the above print result we saw that max_val was around 0.99 when it had
    # a match for sure and around 0.61 when it was unsure. So our 0.7 is still good.

    mouseX = max_loc[0]+50
    mouseY = max_loc[1]+50
 
    # Let's only do something if we are confident on a match
    # Again, this is playing the mini test game random click button :)
    if max_val >= 0.7:
        print("[FOUND IMAGE TEMPLATE] clicking button :)")

        # Lets move the mouse :D There are 2 examples, again one is for right now the other
        # will somewhat simulate a real human to avoid detection etc.

        auto.moveTo(mouseX, mouseY)
        # auto.moveTo(mouseX, mouseY, random.uniform( 0.05, 0.2 ))
        auto.click()
