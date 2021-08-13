# EZImageEdit
A lightweight python image editing program

Requires the following modules to be installed:
-cmu_112_graphics (script incluede)

-numpy

-cv2

<User Instructions>

##### Landing screen #####
>Using the folder icon, you can use the OS file explorer to select a desired image

>Confirm your selection to enter the editing area

##### Editing screen #####
>You will find common image adjustment parameters (brightness, saturation, contrast, sharpening) use the sliders to adjust them.

>Two filters are included, use as you wish.

>At any point you may click the Undo button or use the keyboard shortcut "Control-Z" to undo the previous adjustment.

>Once you're satisfied with your adjustments, click "Export" to go to the export screen. Alternatively, if you wish to save
a preview-quality(lower resolution) version of your work, click "Quick Save" or the "S" key and choose the directory to which 
the image will be saved.

>If you wish to work on a new image, press "R" to return the program to the landing screen.

##### Export Screen #####
>If you landed here by mistake, or simply wish to make additional adjustments to your image, click "cancel" to go back to
the previous screen, all your adjustments are still in place.

>Here you will find the resolution of the exported image. It is set to the same resolution as the original file by default,
however, if you wish to change the export resolution, click on either the width or the length region and specify the dimension,
the aspect ratio of the image is locked, so the other dimension will be calculated automatically.

>You may also choose one of the three interpolation method if you're upscaling. "Nearest Neighbor" is selected by default,
since this is the fastest method, if you prefer higher quality but longer rendering time, you may choose "Bilinear (slow)"
or "Bicubic (very slow)."

>Once the image is rendered, OS file explorer will prompt you to save the result to your specified directory.

Thanks, and have a nice day!
