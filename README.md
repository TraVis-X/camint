Mechanism for traffic counter with Open CV:

1. Take a captured video for processing
  Here motion2.mp4 is used.We can also replace this with live video captured from the camera.
2. Subtract the background to determine all motion objects in video frame
  We can also use our own image for the background.We just need to introduce the image in the argument of fgbg.apply() function.
3. Morphological Transformation-
  Now in the mask matrix we have the frame subtracted from the background.
  This result has a lot of noise in it.So for removing the noise present in the background images we need erosion and for removing noise present in motion objects we need dilation.Also cv2.morphologyEx and cv2.MORPH_OPEN can do the same for renmoving the noise.
4. Contours for motion objects-
  Now with findcontours command we can find all the contours in the frame.
  For all contours with area greater than 2000 can be considered as a vehicle.
5. Centroid of contours-
  To find the coordinates and width and height of the contours we have used cv2.boundingRect() function and to draw a rectangle over the contour cv2.Rectangle() function is used.
   We have x,y as the coordinates of the contour and w,h as rectangle width and height.
   So, (x+w/2,y+h/2) represents coordinate of the centroid of contour.
   
   
