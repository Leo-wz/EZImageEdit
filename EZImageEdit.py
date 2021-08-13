from cmu_112_graphics import *
import numpy as np
import cv2
#3 Sample images included for testing purposes
#Sample 1 https://fujifilm-x.com/wp-content/uploads/2021/01/gfx100s_sample_04_thum-1.jpg
#Sample 2 https://4.img-dpreview.com/files/p/E~TS590x0~articles/3925134721/0266554465.jpeg
#Sample 3 https://washingtonindependent.com/static/ac690e6551a36b0b9e50e370b0827be0/465f1/luca-bravo-zajdgnxsmeg-unsplash.webp

##########################################
# Welcome Screen Mode
##########################################

def welcomeScreenMode_redrawAll(app, canvas):
    ######Welcome Text######
    font = 'Arial 26 bold'
    canvas.create_text(640, 150, text='Welcome to EZImageEdit', font=font, anchor="s")
    canvas.create_text(320, 350, text='Open an image file: ', font=font, anchor="s")

    ######Folder icon######
    #create visual indication that user is hovering over folder icon
    folderx0, foldery0, folderx1, foldery1 = app.button["Folder"]
    canvas.create_rectangle(folderx0, foldery0, folderx1, foldery1,fill=app.buttonColor["Folder"], outline="")
    canvas.create_image(folderx0+25, foldery0+20, image=ImageTk.PhotoImage(app.folderIcon))
    
    ######Confirm button######
    #create visual indication that user is hovering over confirm icon
    confirmx0, confirmy0, confirmx1, confirmy1 = app.button["Confirm"]
    canvas.create_rectangle(confirmx0, confirmy0, confirmx1, confirmy1,fill=app.buttonColor["Confirm"])
    canvas.create_text(midpoint(confirmx0, confirmx1), midpoint(confirmy0, confirmy1), text="Confirm",font="Arial 14 bold", anchor="c")

    ######Path text box######
    canvas.create_rectangle(500, 310, 1000, 350)
    if app.imagePath is not None:
        canvas.create_text(510, 330, text=f"{app.imagePath}", font="Arial 14", anchor="w")

def welcomeScreenMode_mousePressed(app, event):
    #check for click on folder icon
    if inButton(app, event.x, event.y, "Folder"):
    #File selection with OS file explorer, adopted from:
    #https://docs.python.org/3/library/dialog.html
        app.imagePath = filedialog.askopenfilename()
    #check for click on confirm button
    if inButton(app, event.x, event.y, "Confirm"):
        #Error catching
        if app.imagePath is not None and app.imagePath != "":
            #cache original image
            app.originalImage = app.loadImage(app.imagePath)
            imageWidth, imageHeight = app.originalImage.size
            longerside = max(imageWidth, imageHeight)
            #rescale the longer side of image to 700 px to display in editing canvas
            #method adopted from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#loadImageUsingFile
            app.imageToEdit = app.scaleImage(app.originalImage, 750/longerside)
            app.imageWidth, app.imageHeight = app.imageToEdit.size
            app.imageToShow = app.imageToEdit
            app.mode = "editMode"
        else:
            #Show message feature from course material
            #https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#cachingPhotoImages
            app.showMessage("Select an image before continuing")

def welcomeScreenMode_mouseMoved(app, event):
    if inButton(app, event.x, event.y, "Folder"):
        app.buttonColor["Folder"] = "light blue"
    else:
        app.buttonColor["Folder"] = "white"
    if inButton(app, event.x, event.y, "Confirm"):
        app.buttonColor["Confirm"] = "grey"
    else:
        app.buttonColor["Confirm"] = "light grey"

##########################################
# Edit Mode
##########################################
def editMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawQuickSaveButton(app, canvas)
    drawUndoButton(app, canvas)
    drawExportButton(app, canvas)
    drawNoneFilter(app, canvas)
    drawMonoChromeFilter(app, canvas)
    drawbwWaterPaintFilter(app, canvas)
    drawImage(app, canvas)
    drawBrightnessSlider(app, canvas)
    drawContrastSlider(app, canvas)
    drawSharpenSelect(app, canvas)
    drawSaturationSlider(app, canvas)

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="light grey")

def drawImage(app, canvas):
    #Tkinter image method from lecture
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#cachingPhotoImages
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.imageToShow))

def drawQuickSaveButton(app, canvas):
    x0, y0, x1, y1 = app.button.get("QuickSave")
    color = app.buttonColor["QuickSave"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color)
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text="Quick Save",font="Arial 13", anchor="c")

def drawUndoButton(app, canvas):
    x0, y0, x1, y1 = app.button.get("Undo")
    color = app.buttonColor["Undo"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color)
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text="Undo↵",font="Arial 13", anchor="c")

def drawExportButton(app, canvas):
    x0, y0, x1, y1 = app.button.get("Export")
    color = app.buttonColor["Export"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color)
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text="Export",font="Arial 13", anchor="c")

def drawBrightnessSlider(app, canvas):
    x0, y0, x1, y1 = app.button["BrightnessSlider"]
    x2, y2, x3, y3 = app.button["BrightnessSliderButton"]
    buttonCenter = midpoint(x2, x3)
    sliderCenter = midpoint(x0, x1)
    sliderValue = buttonCenter - sliderCenter
    canvas.create_rectangle(x0, y0, x1, y1, fill=app.buttonColor["BrightnessSlider"])
    canvas.create_rectangle(x2, y2, x3, y3, fill=app.buttonColor["BrightnessSliderButton"])
    canvas.create_text(sliderCenter, y0-5, text=f"Brightness",anchor="s", font="Arial 10")
    canvas.create_text(x1, y0, text=f"{sliderValue}",anchor="s", font="Arial 10")

def drawContrastSlider(app, canvas):
    x0, y0, x1, y1 = app.button["ContrastSlider"]
    x2, y2, x3, y3 = app.button["ContrastSliderButton"]
    buttonCenter = midpoint(x2, x3)
    sliderCenter = midpoint(x0, x1)
    sliderValue = buttonCenter - sliderCenter
    canvas.create_rectangle(x0, y0, x1, y1, fill=app.buttonColor["ContrastSlider"])
    canvas.create_rectangle(x2, y2, x3, y3, fill=app.buttonColor["ContrastSliderButton"])
    canvas.create_text(sliderCenter, y0-5, text=f"Contrast",anchor="s", font="Arial 10")
    canvas.create_text(x1, y0, text=f"{sliderValue}",anchor="s", font="Arial 10")

def drawSaturationSlider(app, canvas):
    x0, y0, x1, y1 = app.button["SaturationSlider"]
    x2, y2, x3, y3 = app.button["SaturationSliderButton"]
    buttonCenter = midpoint(x2, x3)
    sliderCenter = midpoint(x0, x1)
    sliderValue = buttonCenter - sliderCenter
    canvas.create_rectangle(x0, y0, x1, y1, fill=app.buttonColor["SaturationSlider"])
    canvas.create_rectangle(x2, y2, x3, y3, fill=app.buttonColor["SaturationSliderButton"])
    canvas.create_text(sliderCenter, y0-5, text=f"Saturation",anchor="s", font="Arial 10")
    canvas.create_text(x1, y0, text=f"{sliderValue}",anchor="s", font="Arial 10")

def drawSharpenSelect(app, canvas):
    x0, y0, x1, y1 = app.button.get("NoneSharp")
    x2, y2, x3, y3 = app.button.get("LowSharp")
    x4, y4, x5, y5 = app.button.get("MediumSharp")
    x6, y6, x7, y7 = app.button.get("HighSharp")
    canvas.create_text(midpoint(x0, x7), midpoint(y6, y7) - 20, text=f"Sharpening filter",anchor="c", font="Arial 13")
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1) + 15, text=f"None",anchor="c", font="Arial 10")
    canvas.create_text(midpoint(x2, x3), midpoint(y2, y3) + 15, text=f"Low",anchor="c", font="Arial 10")
    canvas.create_text(midpoint(x4, x5), midpoint(y4, y5) + 15, text=f"Medium",anchor="c", font="Arial 10")
    canvas.create_text(midpoint(x6, x7), midpoint(y6, y7) + 15, text=f"High",anchor="c", font="Arial 10")
    canvas.create_rectangle(x0, y0, x1, y1, fill=app.buttonColor["NoneSharp"])
    canvas.create_rectangle(x2, y2, x3, y3, fill=app.buttonColor["LowSharp"])
    canvas.create_rectangle(x4, y4, x5, y5, fill=app.buttonColor["MediumSharp"])
    canvas.create_rectangle(x6, y6, x7, y7, fill=app.buttonColor["HighSharp"])

def drawNoneFilter(app, canvas):
    x0, y0, x1, y1 = app.button.get("None")
    color = app.buttonColor["None"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color, outline="")
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text="None",font="Arial 13", anchor="c")
    canvas.create_text(x0-10, midpoint(y0, y1), text="Filters:",font="Arial 13 bold", anchor="e")

def drawMonoChromeFilter(app, canvas):
    x0, y0, x1, y1 = app.button.get("Monochrome")
    color = app.buttonColor["Monochrome"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color, outline="")
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text="Monochrome",font="Arial 13", anchor="c")

def drawbwWaterPaintFilter(app, canvas):
    x0, y0, x1, y1 = app.button.get("BWPaint")
    color = app.buttonColor["BWPaint"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color, outline="")
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text="B&W Paint",font="Arial 13", anchor="c")

def editMode_mouseMoved(app, event):
    #check for mouse on icons
    if inButton(app, event.x, event.y, "QuickSave"):
        app.buttonColor["QuickSave"] = "light green"
    elif inButton(app, event.x, event.y, "Undo"):
        app.buttonColor["Undo"] = "yellow"
    elif inButton(app, event.x, event.y, "Export"):
        app.buttonColor["Export"] = "light green"
    elif inButton(app, event.x, event.y, "BrightnessSliderButton"):
        app.buttonColor["BrightnessSliderButton"] = "brown"   
    elif inButton(app, event.x, event.y, "ContrastSliderButton"):
        app.buttonColor["ContrastSliderButton"] = "brown" 
    elif inButton(app, event.x, event.y, "SaturationSliderButton"):
        app.buttonColor["SaturationSliderButton"] = "brown" 
    
    else:
        app.buttonColor["QuickSave"] = \
        app.buttonColor["Undo"] = \
        app.buttonColor["Export"] = "white"
        app.buttonColor["BrightnessSliderButton"] = \
        app.buttonColor["ContrastSliderButton"] = \
        app.buttonColor["SaturationSliderButton"] = "black"

    #Give visual indication of currently selected filter
    if app.currentFilter == "None":
        app.buttonColor["None"] = "light green"
    elif inButton(app, event.x, event.y, "None"):
        app.buttonColor["None"] = "light blue" 
    else:
        app.buttonColor["None"] = "white"
    if app.currentFilter == "Monochrome":
        app.buttonColor["Monochrome"] = "light green"
    elif inButton(app, event.x, event.y, "Monochrome"):
        app.buttonColor["Monochrome"] = "light blue" 
    else:
        app.buttonColor["Monochrome"] = "white"
    if app.currentFilter == "BWPaint":
        app.buttonColor["BWPaint"] = "light green"
    elif inButton(app, event.x, event.y, "BWPaint"):
        app.buttonColor["BWPaint"] = "light blue" 
    else:
        app.buttonColor["BWPaint"] = "white"
    
    #Give visual indication of currently selected sharpening filter
    if app.currentSharp == "NoneSharp":
        app.buttonColor["NoneSharp"] = "blue"
    elif inButton(app, event.x, event.y, "NoneSharp"):
        app.buttonColor["NoneSharp"] = "light blue" 
    else:
        app.buttonColor["NoneSharp"] = "white"
    if app.currentSharp == "LowSharp":
        app.buttonColor["LowSharp"] = "blue"
    elif inButton(app, event.x, event.y, "LowSharp"):
        app.buttonColor["LowSharp"] = "light blue" 
    else:
        app.buttonColor["LowSharp"] = "white"
    if app.currentSharp == "MediumSharp":
        app.buttonColor["MediumSharp"] = "blue"
    elif inButton(app, event.x, event.y, "MediumSharp"):
        app.buttonColor["MediumSharp"] = "light blue" 
    else:
        app.buttonColor["MediumSharp"] = "white"
    if app.currentSharp == "HighSharp":
        app.buttonColor["HighSharp"] = "blue"
    elif inButton(app, event.x, event.y, "HighSharp"):
        app.buttonColor["HighSharp"] = "light blue" 
    else:
        app.buttonColor["HighSharp"] = "white"

def editMode_mousePressed(app, event):
    #check for click on quicksave button
    if inButton(app, event.x, event.y, "QuickSave"):
        quickSave(app)
    #check for undo button
    elif inButton(app, event.x, event.y, "Undo"):
        rollback(app)
    #check for export button
    elif inButton(app, event.x, event.y, "Export"):
        app.exportWidth, app.exportHeight = app.originalImage.size
        app.mode = "exportMode"
    #check for None filter selection
    elif inButton(app, event.x, event.y, "None"):
        app.currentFilter = "None"
    #check for monochrome filter selection
    elif inButton(app, event.x, event.y, "Monochrome"):
        app.currentFilter = "Monochrome"
    #check for B&W Paint filter selection
    elif inButton(app, event.x, event.y, "BWPaint"):
        app.currentFilter = "BWPaint"
    #check for Brightness Adjustment
    elif inButton(app, event.x, event.y, "BrightnessSlider") or\
         inButton(app, event.x, event.y, "BrightnessSliderButton"):
        app.canMove = True
        app.buttonToMove = "BrightnessSliderButton"
    #check for Contrast Adjustment
    elif inButton(app, event.x, event.y, "ContrastSlider") or\
         inButton(app, event.x, event.y, "ContrastSliderButton"):
        app.canMove = True
        app.buttonToMove = "ContrastSliderButton"
    #check for Saturation Adjustment
    elif inButton(app, event.x, event.y, "SaturationSlider") or\
         inButton(app, event.x, event.y, "SaturationSliderButton"):
        app.canMove = True
        app.buttonToMove = "SaturationSliderButton"
    #check for Sharpening Adjustment
    elif inButton(app, event.x, event.y, "NoneSharp"):
        app.currentSharp = "NoneSharp"
    elif inButton(app, event.x, event.y, "LowSharp"):
        app.currentSharp = "LowSharp"
    elif inButton(app, event.x, event.y, "MediumSharp"):
        app.currentSharp = "MediumSharp"
    elif inButton(app, event.x, event.y, "HighSharp"):
        app.currentSharp = "HighSharp"
    if app.buttonToMove is not None:
        moveButton(app, event, app.buttonToMove)
    brightnessAdjValue = checkAdjValue(app, "BrightnessSliderButton")
    contrastAdjValue = checkAdjValue(app, "ContrastSliderButton")
    saturationAdjValue = checkAdjValue(app, "SaturationSliderButton")
    sharpenAdjValue = checkSharpenVal(app)
    applyFilter = app.currentFilter
    makeAdjustment(app,
                   brightnessAdjValue,
                   contrastAdjValue,
                   saturationAdjValue,
                   sharpenAdjValue,
                   applyFilter)

#Due to poor runtime performance of sharpening filter, reducing the available levels
#of sharpness adjustment to 4 significantly improves performance
def checkSharpenVal(app):
    if app.currentSharp == "NoneSharp":
        value = 0
    elif app.currentSharp == "LowSharp":
        value = 33
    elif app.currentSharp == "MediumSharp":
        value = 67
    elif app.currentSharp == "HighSharp":
        value = 100
    return value

def editMode_mouseDragged(app, event):
    if app.canMove:
        moveButton(app, event, app.buttonToMove)
        brightnessAdjValue = checkAdjValue(app, "BrightnessSliderButton")
        contrastAdjValue = checkAdjValue(app, "ContrastSliderButton")
        saturationAdjValue = checkAdjValue(app, "SaturationSliderButton")
        sharpenAdjValue = checkSharpenVal(app)
        applyFilter = app.currentFilter
        makeAdjustment(app,
                    brightnessAdjValue,
                    contrastAdjValue,
                    saturationAdjValue,
                    sharpenAdjValue,
                    applyFilter)

def editMode_mouseReleased(app, event):
    #slider cannot move once released
    app.canMove = False
    app.buttonToMove = None
    #Push changes to save state list
    if not inButton(app, event.x, event.y, "Undo"):
        brightnessAdjValue = checkAdjValue(app, "BrightnessSliderButton")
        contrastAdjValue = checkAdjValue(app, "ContrastSliderButton")
        saturationAdjValue = checkAdjValue(app, "SaturationSliderButton")
        applyFilter = app.currentFilter
        app.saveState.append((brightnessAdjValue,
                              contrastAdjValue, 
                              saturationAdjValue, 
                              app.currentSharp, 
                              applyFilter))
    #allow up to 8 undo state
    if len(app.saveState) > 8:
        app.saveState.pop(0)

def editMode_keyPressed(app, event):
    #return the app to initial screen if user wish to reset
    if event.key == "r":
        appStarted(app)
    #Keyboard shortcut--quick save with s
    if event.key == "s":
        quickSave(app)
    #control-z reverse last adjustment
    if event.key == "control-z":
        rollback(app)

def moveButton(app, event, button):
    x0, y0, x1, y1 = app.button["BrightnessSlider"]
    x2, y2, x3, y3 = app.button[button]
    if event.x < x0:
        event.x = x0
    elif event.x > x1:
        event.x = x1
    app.button[button] = (event.x-3, y2, event.x+3, y3)

#Numpy documentation references
#https://numpy.org/doc/stable/reference/generated/numpy.asarray.html
#https://numpy.org/doc/stable/user/basics.types.html
def makeAdjustment(app,
                   brightnessAdjValue,
                   contrastAdjValue,
                   saturationAdjValue,
                   sharpenAdjValue,
                   applyFilter):
    #Selective rendering of pixels to improve efficiency
    #Convert photo to Numpy array, use int32 format to prevernt overflow
    cache = np.asarray(app.imageToEdit).astype(np.int32)
    if brightnessAdjValue != 0:
        cache = brightnessAdj(cache, brightnessAdjValue)
    if contrastAdjValue != 0:
        cache = contrastAdj(cache, contrastAdjValue)
    if saturationAdjValue != 0:
        cache = saturationAdj(cache, saturationAdjValue)
    if sharpenAdjValue != 0:
        cache = sharpenAdj(cache, sharpenAdjValue)
    if applyFilter == "Monochrome":
        cache = monoChromeFilter(cache)
    elif applyFilter == "BWPaint":
        cache = bwWaterPaintFilter(cache)
    #Back to image for display
    cache = cache.astype(np.uint8)
    cache = Image.fromarray(cache, "RGB")
    app.imageToShow = cache
    

#Undo feature using saved states
def rollback(app):
    #safeguard for empty savestate
    if len(app.saveState) == 1:
        return
    app.saveState.pop()
    brightnessAdjValue = app.saveState[-1][0]
    contrastAdjValue = app.saveState[-1][1]
    saturationAdjValue = app.saveState[-1][2]
    app.currentSharp = app.saveState[-1][3]
    sharpenAdjValue = checkSharpenVal(app)
    app.currentFilter = applyFilter = app.saveState[-1][4]
    makeAdjustment(app,
                    brightnessAdjValue,
                    contrastAdjValue,
                    saturationAdjValue,
                    sharpenAdjValue,
                    applyFilter)
    x0, y0, x1, y1 = app.button["BrightnessSlider"]
    x2, y2, x3, y3 = app.button["BrightnessSliderButton"]
    x4, y4, x5, y5 = app.button["ContrastSliderButton"]
    x6, y6, x7, y7 = app.button["SaturationSliderButton"]

    SliderCenter = midpoint(x0, x1)
    #Re-position sliders
    x2 = SliderCenter + brightnessAdjValue - 3
    x3 = SliderCenter + brightnessAdjValue + 3
    x4 = SliderCenter + contrastAdjValue - 3
    x5 = SliderCenter + contrastAdjValue + 3
    x6 = SliderCenter + saturationAdjValue - 3
    x7 = SliderCenter + saturationAdjValue + 3

    app.button["BrightnessSliderButton"] = x2, y2, x3, y3
    app.button["ContrastSliderButton"] = x4, y4, x5, y5
    app.button["SaturationSliderButton"] = x6, y6, x7, y7

def brightnessAdj(image, AdjValue):
    #Numpy documentation references
    #https://numpy.org/doc/stable/reference/generated/numpy.asarray.html
    #https://numpy.org/doc/stable/user/basics.types.html

    
    #Use adjustment layer to adjust brightness
    adjLayer = np.full_like(image, AdjValue)
    image += adjLayer
    #Cap value at 255
    image = np.clip(image, 0, 255)
    return image


def contrastAdj(image, AdjValue):
    #See above for Numpy references
    #Correction factor calculation formula adopted from:
    #https://athena.ecs.csus.edu/~changw/ImageProcessing/basic-techniques/5-Contrast-Adjustment.pdf
    factor = 259*(255+AdjValue)/(255*(259-AdjValue))
    image = (image-128)*factor+128
    image = np.clip(image, 0, 255)
    return image

def saturationAdj(image, AdjValue):
    #See above for Numpy references
    #Based on color theory http://web.mit.edu/6.813/www/sp16/classes/16-color/
    #I derived the following formula for adjusting color saturation
    #We expect an image of -100 saturation to be a greyscale image
    #and +100 to be twice the perceived color intensity, therefore decreasing
    #saturation means decreasing the color value's departure from the mean of
    #(r,g,b)--in case of -100 saturation, r=g=b. Increasing saturation should
    #have the opposite effect. Because the departure from mean for each of r,g,b
    #is different, the "step" of adjustment should be different for each.
    

    #Create separate layers for each channel to adjust
    r = np.full_like(image, image)
    g = np.full_like(image, image)
    b = np.full_like(image, image)
    r[:,:,2] = r[:,:,1] = r[:,:,0]
    g[:,:,2] = r[:,:,0] = r[:,:,1]
    b[:,:,1] = r[:,:,0] = r[:,:,2]
    luminance = r/3+g/3+b/3
    #Compute adjustment layer for each channel
    rIncrement = (r-luminance)/100
    gIncrement = (g-luminance)/100
    bIncrement = (b-luminance)/100
    adjLayer = np.full_like(image, AdjValue)
    r = r+rIncrement * adjLayer
    g = g+gIncrement * adjLayer
    b = b+bIncrement * adjLayer
    #Stack method from https://numpy.org/doc/stable/reference/generated/numpy.stack.html
    image = np.stack((r[:,:,0],g[:,:,1],b[:,:,2]), axis=-1)
    image = np.clip(image, 0, 255)

    return image


def sharpenAdj(image, AdjValue):
    #See above for Numpy references
    intermediate = convolution(image)
    adjLayer = np.full_like(image, AdjValue)
    #Blend the sharpened and original image using weights derived from adjValue
    image = image * (1 - adjLayer / 100) + intermediate * adjLayer / 100
    image = np.clip(image, 0, 255)
    return image

'''Using suggested sharpen kernal(convolution matrix)
                                | 0  -1  0 |
                                |-1   5 -1 |
                                | 0  -1  0 | from
https://en.wikipedia.org/wiki/Kernel_(image_processing)
 '''
#perform convolution on image using given kernal
def convolution(image):
    #See previous functions for Numpy references
    r = np.full_like(image, image)
    g = np.full_like(image, image)
    b = np.full_like(image, image)
    #Create separate channels for array operations
    newr = np.full_like(image, image)
    newg = np.full_like(image, image)
    newb = np.full_like(image, image)
    top = np.full_like(image, image)
    #Remove side to prevent out of bound error
    top = top[0:-3,1:-2,:]
    bottom = np.full_like(image, image)
    bottom = bottom[2:-1,1:-2,:]
    left = np.full_like(image, image)
    left = left[1:-2,0:-3,:]
    right = np.full_like(image, image)
    right = right[1:-2,2:-1,:]
    mid = np.full_like(image, 5)
    mid = mid[1:-2,1:-2,:]
    side = np.full_like(image, -1)
    side = side[1:-2,1:-2,:]
    #Perform convolution based on the provided kernal
    newr[1:-2,1:-2,:] = r[1:-2,1:-2,:] * mid + top * side + bottom * side + left * side + right * side
    newg[1:-2,1:-2,:] = g[1:-2,1:-2,:] * mid + top * side + bottom * side + left * side + right * side
    newb[1:-2,1:-2,:] = b[1:-2,1:-2,:] * mid + top * side + bottom * side + left * side + right * side
    image = np.stack((newr[:,:,0],newg[:,:,1],newb[:,:,2]), axis=-1)
    #Return raw array data back
    return image
    
def checkAdjValue(app, button):
    x0, y0, x1, y1 = app.button["BrightnessSlider"]
    x2, y2, x3, y3 = app.button[button]
    buttonCenter = midpoint(x2, x3)
    sliderCenter = midpoint(x0, x1)
    return buttonCenter - sliderCenter

def monoChromeFilter(image):
    #See previous functions for Numpy references
    #MonoChrome filter essentially removes color from the image while retaining
    #apparant brightness(mean of rgb) 

    #Create separate layers for each channel to adjust
    r = np.full_like(image, image)
    g = np.full_like(image, image)
    b = np.full_like(image, image)
    r[:,:,2] = r[:,:,1] = r[:,:,0]
    g[:,:,2] = r[:,:,0] = r[:,:,1]
    b[:,:,1] = r[:,:,0] = r[:,:,2]
    luminance = (r+g+b)/3
    luminance = np.clip(luminance, 0, 255)
    #Equalize R/G/B value
    luminance[:,:,2] = luminance[:,:,1] = luminance[:,:,0]

    return luminance

def bwWaterPaintFilter(image):
    #See previous functions for Numpy references
    #Water paint effect can be achieved by bit depth compression

    #Create separate layers for each channel to adjust
    r = np.full_like(image, image)
    g = np.full_like(image, image)
    b = np.full_like(image, image)
    r[:,:,2] = r[:,:,1] = r[:,:,0]
    g[:,:,2] = r[:,:,0] = r[:,:,1]
    b[:,:,1] = r[:,:,0] = r[:,:,2]
    luminance = (r+g+b)/3
    luminance = luminance//64*64
    luminance = np.clip(luminance, 0, 255)
    #Equalize R/G/B value
    luminance[:,:,2] = luminance[:,:,1] = luminance[:,:,0]

    return luminance


#Save current preview to specified path and name, no modification to size
def quickSave(app):
    #Return file name&path with OS file explorer, adopted from:
    #https://docs.python.org/3/library/dialog.html
    savePath = filedialog.asksaveasfilename(filetypes=[('JPEG', '*.jpg')], defaultextension=".jpg")
    if savePath != "":
        app.imageToShow.save(f"{savePath}")

##########################################
# Export Mode
##########################################
def exportMode_redrawAll(app, canvas):
    drawSaveOptions(app, canvas)
    drawCancelButton(app, canvas)
    drawConfirmExportButton(app, canvas)
    drawResolution(app, canvas)
    drawNoInterpolation(app, canvas)
    drawBilinear(app, canvas)
    drawBicubic(app, canvas)

def drawSaveOptions(app, canvas):
        canvas.create_rectangle(app.width/2 - 200, app.height/2 - 300,
                                app.width/2 + 200, app.height/2 + 300,
                                fill="grey", outline="")

def drawCancelButton(app, canvas):
    x0, y0, x1, y1 = app.button.get("Cancel")
    color = app.buttonColor["Cancel"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color)
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text="cancel",font="Arial 13", anchor="c")

def drawConfirmExportButton(app, canvas):
    x0, y0, x1, y1 = app.button.get("ConfirmExport")
    color = app.buttonColor["ConfirmExport"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color)
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text="Export",font="Arial 13", anchor="c")

def drawResolution(app, canvas):
    drawWidthBox(app, canvas, app.exportWidth)
    drawHeightBox(app, canvas, app.exportHeight)
    canvas.create_text(app.width/2, app.height/2 - 235, text="X", anchor="c")
    canvas.create_text(app.width/2, app.height/2 - 200, text="Aspect ratio is locked", font="Arial 13 bold", anchor="c")

def drawWidthBox(app, canvas, width):
    x0, y0, x1, y1 = app.button.get("Width")
    color = app.buttonColor["Width"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color)
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text=width,font="Arial 13", anchor="c")
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1) - 30, text="Width",font="Arial 13", anchor="c")
    canvas.create_text(x0 - 20, midpoint(y0, y1), text="Resolution", font="Arial 13 bold", anchor="e")

def drawHeightBox(app, canvas, Height):
    x0, y0, x1, y1 = app.button.get("Height")
    color = app.buttonColor["Height"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color)
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text=Height,font="Arial 13", anchor="c")
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1) - 30, text="Height",font="Arial 13", anchor="c")

def drawNoInterpolation(app, canvas):
    x0, y0, x1, y1 = app.button.get("InterNone")
    color = app.buttonColor["InterNone"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color, outline="")
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text="Nearest neighbor",font="Arial 13", anchor="c")
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1) - 30, text="Interpolation Method",font="Arial 14", anchor="c")

def drawBilinear(app, canvas):
    x0, y0, x1, y1 = app.button.get("InterBilinear")
    color = app.buttonColor["InterBilinear"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color, outline="")
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text="Bilinear(slow)",font="Arial 13", anchor="c")

def drawBicubic(app, canvas):
    x0, y0, x1, y1 = app.button.get("InterBicubic")
    color = app.buttonColor["InterBicubic"]
    canvas.create_rectangle(x0, y0, x1, y1,fill=color, outline="")
    canvas.create_text(midpoint(x0, x1), midpoint(y0, y1), text="Bicubic(very slow)",font="Arial 13", anchor="c")

def exportMode_mouseMoved(app, event):
    #check for mouse on icons
    if inButton(app, event.x, event.y, "Cancel"):
        app.buttonColor["Cancel"] = "orange"
    elif inButton(app, event.x, event.y, "ConfirmExport"):
        app.buttonColor["ConfirmExport"] = "light green"
    elif inButton(app, event.x, event.y, "Width"):
        app.buttonColor["Width"] = "light blue"
    elif inButton(app, event.x, event.y, "Height"):
        app.buttonColor["Height"] = "light blue"
    else:
        app.buttonColor["Cancel"] = \
        app.buttonColor["ConfirmExport"] = "light grey"
        app.buttonColor["Width"] = \
        app.buttonColor["Height"] = "white"
    #Give visual indication of currently selection interpolation method
    if app.currentInter == "NearestNeighbor":
        app.buttonColor["InterNone"] = "light green"
    elif inButton(app, event.x, event.y, "InterNone"):
        app.buttonColor["InterNone"] = "light blue" 
    else:
        app.buttonColor["InterNone"] = "white"
    if app.currentInter == "Bilinear":
        app.buttonColor["InterBilinear"] = "light green"
    elif inButton(app, event.x, event.y, "InterBilinear"):
        app.buttonColor["InterBilinear"] = "light blue" 
    else:
        app.buttonColor["InterBilinear"] = "white"
    if app.currentInter == "Bicubic":
        app.buttonColor["InterBicubic"] = "light green"
    elif inButton(app, event.x, event.y, "InterBicubic"):
        app.buttonColor["InterBicubic"] = "light blue" 
    else:
        app.buttonColor["InterBicubic"] = "white"
        
def exportMode_mousePressed(app, event):
    #check for click on quicksave button
    if inButton(app, event.x, event.y, "Cancel"):
        app.mode = "editMode"
    #check for No interpolation (nearest neighbor) selection
    if inButton(app, event.x, event.y, "InterNone"):
        app.currentInter = "NearestNeighbor"
    #check for Bilinear interpolation selection
    elif inButton(app, event.x, event.y, "InterBilinear"):
        app.currentInter = "Bilinear"
    #check for Bicubic interpolation selection
    elif inButton(app, event.x, event.y, "InterBicubic"):
        app.currentInter = "Bicubic"
    #Check for width and height change
    elif inButton(app, event.x, event.y, "Width"):
        #getUserInput feature adopted from
        #https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#cachingPhotoImages
        inputWidth = app.getUserInput("Input desired width")
        if inputWidth is None:
            return
        else:
            ratio = app.exportWidth/app.exportHeight
            app.exportWidth = int(inputWidth)
            app.exportHeight = int(app.exportWidth/ratio)
    elif inButton(app, event.x, event.y, "Height"):
        inputHeight = app.getUserInput("Input desired height")
        if inputHeight is None:
            return
        else:
            ratio = app.exportWidth/app.exportHeight
            app.exportHeight = int(inputHeight)
            app.exportWidth = int(app.exportHeight * ratio)
    elif inButton(app, event.x, event.y, "ConfirmExport"):
        app.showMessage("rendering final image...\nlarge image will take significantly longer\nclick OK to start")
        resultImage = finalAdjustment(app)
        properSave(resultImage)

def finalAdjustment(app):
    #Get the adjustments made on the preview canvas, and apply those adjustments
    #on the original image
    #Similar format to the makeAdjustment function
    bAdjVal, cAdjVal, sAdjVal, sharpen, applyFilter = app.saveState[-1]
    shAdjVal = checkSharpenVal(app)
    cache = np.asarray(app.originalImage).astype(np.int32)
    if bAdjVal != 0:
        cache = brightnessAdj(cache, bAdjVal)
    if cAdjVal != 0:
        cache = contrastAdj(cache, cAdjVal)
    if sAdjVal != 0:
        cache = saturationAdj(cache, sAdjVal)
    if shAdjVal != 0:
        cache = sharpenAdj(cache, shAdjVal)
    if applyFilter == "Monochrome":
        cache = monoChromeFilter(cache)
    elif applyFilter == "BWPaint":
        cache = bwWaterPaintFilter(cache)
    cache = cache.astype(np.uint8)
    cache = Image.fromarray(cache, "RGB")
    if (app.exportWidth, app.exportHeight) != app.originalImage.size:
        cache = performInterpolation(app, cache, app.exportWidth, app.exportHeight, app.currentInter)
    return cache

def properSave(image):
    #Return file name&path with OS file explorer, adopted from:
    #https://docs.python.org/3/library/dialog.html
    savePath = filedialog.asksaveasfilename(filetypes=[('JPEG', '*.jpg')], defaultextension=".jpg")
    if savePath != "":
        image.save(f"{savePath}")

def performInterpolation(app, image, width, height, interMethod):
    #Perform nearest neighbor interpolation/#if downscaling, use this method
    if interMethod == "NearestNeighbor" or width < image.width:
        image = nearestNeighbor(app, image, width, height)
    elif interMethod == "Bilinear":
        #Based on the new width, calculate the number of iterations needed
        numIteration = int(width/image.width)
        for i in range(numIteration):
            #Perform n iterations of Bilinear interpolation
            image = bilinear(image)
        #After interpolation, downscale image to the desired resolution.
        image = app.scaleImage(image, width/image.width)
    elif interMethod == "Bicubic":
        image = bicubic(app, image, width, height)
    return image

#The scaleImage method
#adopted from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#loadImageUsingFile
#scale image is a simple image resizer that performs nearest neighbor interpolation
def nearestNeighbor(app, image, width, height):
    result = app.scaleImage(image, width/image.width)
    return result

def bilinear(image):
    oldWidth, oldHeight = image.size
    #Perform 1 iteration of 2x bilinear interpolation
    result = Image.new(mode='RGB', size=(2 * oldWidth, 2 * oldHeight))
    for x in range(image.width):
        for y in range(image.height):
            #First fill in alternating pixels(even pixels in even rows)
            r,g,b = image.getpixel((x,y))
            result.putpixel((x*2,y*2),(r,g,b))
    #Now fill in even number rolls empty pixels by averaging adjacent pixels
    #Right-most column and bottom-most row neglected
    for y in range(0, result.height-1, 2):
        for x in range(1, result.width-1, 2):
            r1,g1,b1 = result.getpixel((x - 1,y))
            r2,g2,b2 = result.getpixel((x + 1,y))
            r3 = int((r1+r2)/2)
            g3 = int((g1+g2)/2)
            b3 = int((b1+b2)/2)
            result.putpixel((x, y),(r3,g3,b3))
    #Now fill in even column even empty pixels by averaging top and bottom pixels
    #Right-most column and bottom-most row still neglected
    for y in range(1, result.height-1, 2):
        for x in range(0, result.width-1, 2):
            r1,g1,b1 = result.getpixel((x, y - 1))
            r2,g2,b2 = result.getpixel((x, y + 1))
            r3 = int((r1+r2)/2)
            g3 = int((g1+g2)/2)
            b3 = int((b1+b2)/2)
            result.putpixel((x, y),(r3,g3,b3))
    #Edge handling
    #Copy left pixels to the right-most column
    for y in range(result.height-1):
        r,g,b = result.getpixel((result.width - 2, y))
        result.putpixel((result.width - 1, y),(r,g,b))
    #Copy upper pixels to the bottom column
    for x in range(result.width - 1):
        r,g,b = result.getpixel((x, result.height - 2))
        result.putpixel((x, result.height - 1),(r,g,b))
    #Handle single empty pixel in lower right corner
    r1,g1,b1 = result.getpixel((result.width - 1, result.height - 2))
    r2,g2,b2 = result.getpixel((result.width - 2, result.height - 1))
    r3 = int((r1+r2)/2)
    g3 = int((g1+g2)/2)
    b3 = int((b1+b2)/2)
    result.putpixel((result.width - 1, result.height - 1),(r3,g3,b3))
    #Finally, fill in odd row odd pixels by averaging pixels in the four corners
    for y in range(1, result.height-1, 2):
        for x in range(1, result.width-1, 2):
            r1,g1,b1 = result.getpixel((x - 1, y - 1))
            r2,g2,b2 = result.getpixel((x + 1, y - 1))
            r3,g3,b3 = result.getpixel((x - 1, y + 1))
            r4,g4,b4 = result.getpixel((x + 1, y + 1))
            r5 = int((r1+r2+r3+r4)/4)
            g5 = int((g1+g2+g3+g4)/4)
            b5 = int((b1+b2+b3+b4)/4)
            result.putpixel((x, y),(r5,g5,b5))
    return result

def bicubic(app, image, width, height):

    #cubic resize adopted from https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html
    scalFactor = width/image.width
    image = np.asarray(image)
    image = cv2.resize(image,None, fx = scalFactor, fy = scalFactor, interpolation = cv2.INTER_CUBIC)
    #fromarray method in pillow documentation
    #https://pillow.readthedocs.io/en/stable/reference/Image.html
    image = Image.fromarray(image)
    return image

##########################################
# Main App
##########################################

def appStarted(app):
    app.mode = "welcomeScreenMode"
    #Folder icon acquired from https://www.iconpacks.net/icons/2/free-folder-icon-1484-thumb.png
    app.folderIcon = app.scaleImage(app.loadImage("folder.png"), 1/12)
    app.imagePath = None
    app.button = dict()
    app.buttonColor = dict()
    app.imageWidth = 0
    app.imageHeight = 0
    app.canMove = False
    app.saveState = [(0, 0, 0, "NoneSharp", None)]
    setButton(app)

######Helper Functions######
def midpoint(num1, num2):
    return (num2 - num1)//2 + num1

def inButton(app, x, y, buttonName):
    x0, y0, x1, y1 = app.button.get(buttonName)
    if x0 < x < x1 and y0 < y < y1:
        return True
    return False

def setButton(app):
    ######Welcome Screen######
    app.button["Confirm"] = (1100, 310, 1200, 350)
    app.buttonColor["Confirm"] = "light grey"
    app.button["Folder"] = (1025, 308, 1075, 350)
    app.buttonColor["Folder"] = "white"
    ######Edit Mode######
    app.button["QuickSave"] = (app.width/25, app.height/15, app.width/25+100, app.height/15+30)
    app.buttonColor["QuickSave"] = "white"
    app.button["Undo"] = (app.width/25, 12*app.height/15, app.width/25+100, 12*app.height/15+30)
    app.buttonColor["Undo"] = "white"
    app.button["Export"] = (app.width/25, app.height/15+50, app.width/25+100, app.height/15+50+30)
    app.buttonColor["Export"] = "white"
    app.button["None"] = (22*app.width/25, 7*app.height/15, 22*app.width/25+100, 7*app.height/15+20)
    app.buttonColor["None"] = "white"
    app.button["Monochrome"] = (22*app.width/25, 7*app.height/15+25, 22*app.width/25+100, 7*app.height/15+45)
    app.buttonColor["Monochrome"] = "white"
    app.button["BWPaint"] = (22*app.width/25, 7*app.height/15+50, 22*app.width/25+100, 7*app.height/15+70)
    app.buttonColor["BWPaint"] = "white"
    app.button["NoneSharp"] = (1050-10, 252-6, 1050+10, 252+6)
    app.buttonColor["NoneSharp"] = "white"
    app.button["LowSharp"] = (1050+66-10, 252-6, 1050+66+10, 252+6)
    app.buttonColor["LowSharp"] = "white"
    app.button["MediumSharp"] = (1050+133-10, 252-6, 1050+133+10, 252+6)
    app.buttonColor["MediumSharp"] = "white"
    app.button["HighSharp"] = (1050+200-10, 252-6, 1050+200+10, 252+6)
    app.buttonColor["HighSharp"] = "white"
    ######Sliders######
    app.button["BrightnessSlider"] = (1050, 98, 1250, 107)
    app.buttonColor["BrightnessSlider"] = "white"
    app.button["BrightnessSliderButton"] = (1147, 95, 1153, 110)
    app.buttonColor["BrightnessSliderButton"] = "black"
    app.button["ContrastSlider"] = (1050, 98+50, 1250, 107+50)
    app.buttonColor["ContrastSlider"] = "white"
    app.button["ContrastSliderButton"] = (1147, 95+50, 1153, 110+50)
    app.buttonColor["ContrastSliderButton"] = "black"
    app.button["SaturationSlider"] = (1050, 98+50+50, 1250, 107+50+50)
    app.buttonColor["SaturationSlider"] = "white"
    app.button["SaturationSliderButton"] = (1147, 95+50+50, 1153, 110+50+50)
    app.buttonColor["SaturationSliderButton"] = "black"
    ######Export Mode######
    app.button["Cancel"] = (app.width/2 - 190, app.height/2 +250, app.width/2 -120, app.height/2 + 280)
    app.buttonColor["Cancel"] = "light grey"
    app.button["ConfirmExport"] = (app.width/2 + 120, app.height/2 +250, app.width/2 + 190, app.height/2 + 280)
    app.buttonColor["ConfirmExport"] = "light grey"
    app.button["Width"] = (app.width/2 - 80, app.height/2 - 250, app.width/2 - 20, app.height/2 - 220)
    app.buttonColor["Width"] = "white"
    app.button["Height"] = (app.width/2 + 20, app.height/2 - 250, app.width/2 + 80, app.height/2 - 220)
    app.buttonColor["Height"] = "white"
    app.button["InterNone"] = (app.width/2 - 70, app.height/2, app.width/2 + 70, app.height/2 + 20)
    app.buttonColor["InterNone"] = "white"
    app.button["InterBilinear"] = (app.width/2 - 70, app.height/2 + 25, app.width/2 + 70, app.height/2 + 45)
    app.buttonColor["InterBilinear"] = "white"
    app.button["InterBicubic"] = (app.width/2 - 70, app.height/2 + 50, app.width/2 + 70, app.height/2 + 70)
    app.buttonColor["InterBicubic"] = "white"
    #Initialize states
    app.buttonToMove = None
    app.currentFilter = "None"
    app.currentInter = "NearestNeighbor"
    app.currentSharp = "NoneSharp"
    

runApp(width=1280, height=720)
