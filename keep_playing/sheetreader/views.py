from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *

from django.http import HttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
import numpy as np
import cv2
from collections import namedtuple
import time
from msvcrt import getch

def index(request):
	sheet_data = Sheet.objects.all()
	return render(request, 'sheetreader/home.html', {'sheet_data': sheet_data})

def sheetReader(request, pk):
	sheet = get_object_or_404(Sheet, pk=pk)
	return render(request, 'sheetreader/reader.html', {'sheet': sheet})

def newSheet(request):
	form = SheetForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save() # saves the object that was just created
			return HttpResponseRedirect(reverse('sheetreader:index')) # once completed, return to home
	return render(request, "sheetreader/sheet_form.html", {'form': form})

def updateSheet(request, pk=None):
	instance = get_object_or_404(Sheet, pk=pk)
	form = SheetForm(request.POST or None, request.FILES or None, instance=instance)
	# if form submission was successful
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('sheetreader:index'))
	return render(request, "sheetreader/sheet_form.html", {'form': form})

def deleteSheets(request):
	items = request.POST.getlist('items') # receives a list of the items through a request.POST
	Sheet.objects.filter(id__in=request.POST.getlist('items')).delete()
	return HttpResponseRedirect(reverse('sheetreader:index'))

#Determines if current list contains a guesture
def checkGuesture(pointsTracking):
    if pointsTracking[0].Pose != "Front":
        return "Null"
    
    frontPreDetected = False
    frontPreCount = 0
    frontPreX = 0

    leftDetected = False
    leftCount = 0
    leftX = 0

    rightDetected = False
    rightCount = 0
    rightX = 0

    frontPostDetected = False
    frontPostCount = 0
    frontPostX = 0

    for point in pointsTracking:
        if point.Pose == "Front":
            if not leftDetected  and not rightDetected :
                frontPreCount += 1
                frontPreX += point.X
                if frontPreCount > 3:
                    frontPreDetected = True
            else:
                frontPostCount += 1
                frontPostX += point.X
                if frontPostCount > 3:
                    frontPostDetected = True
        elif point.Pose == "Left" and frontPreDetected:
            leftCount += 1
            leftX += point.X    
            if leftCount > 3:
                leftDetected = True
        elif point.Pose == "Right" and frontPreDetected:
            rightCount += 1
            rightX += point.X    
            if rightCount > 3:
                rightDetected = True

    if frontPreDetected and frontPostDetected:
        frontPreXAvg = frontPreX / frontPreCount
        frontPostAvg = frontPostX / frontPostCount
        if leftDetected:
            leftXAvg = leftX / leftCount
            if leftXAvg < frontPreXAvg and leftXAvg < frontPostAvg:
                #print("Guesture Left Detected")
                return "Left Detected"
        elif rightDetected:
            rightXAvg = rightX / rightCount
            if rightXAvg > frontPreXAvg and rightXAvg > frontPostAvg:
                #print("Guesture Right Detected")
                return "Right Detected"
    return ""

def trimList(pointsTracking):
    lastTime = pointsTracking[len(pointsTracking) - 1].Time
    trimmed = False
    while not trimmed:
        if (lastTime - pointsTracking[0].Time) > 3:
            pointsTracking.pop(0)
        else: 
            trimmed = True
    return pointsTracking

cap = cv2.VideoCapture(0)
defaultURL = static('haarcascade_frontalface_default.xml')
profileURL = static('haarcascade_profileface.xml')
face_cascade = cv2.CascadeClassifier(defaultURL)
face_cascade_profile = cv2.CascadeClassifier(profileURL)

#Point data structure - tracks position & pose
Point = namedtuple("Point", "X Y Size Pose Time")

#Initiailze camera & classifiers

def readGesture(placeholder):

	#Chronological list of tracking points
	pointsTracking = []
	startTime = time.clock
	while(True):
		#Reads frame from camera & flips to act like mirror
		ret, frame = cap.read()   

		#Checks if frame was read
		if ret:
			frameFlipped = cv2.flip(frame, 1)
			#Converts to greyscale (Quicker processing) & flips to act like a mirror
			gray = cv2.cvtColor(frameFlipped, cv2.COLOR_BGR2GRAY)

			#Detect frontal face
			faces = face_cascade.detectMultiScale(gray, 1.3, 5)
			
			largestFace = Point(0,0,0,"", 0)
			if len(faces) > 0:
				for (x, y, w, h) in faces:
					if(w * h > largestFace.Size):
						largestFace = Point(x, y, w * h, "Front", time.clock())
					cv2.rectangle(frameFlipped, (x,y), (x+w, y+h), (255, 0, 0), 2)
			else:
				#If no frontal face detected, check for profiles of faces
				faces_profile = face_cascade_profile.detectMultiScale(gray, 1.3, 5)

				if len(faces_profile) > 0:
					for (x, y, w, h) in faces_profile:
						if(w * h > largestFace.Size):
							largestFace = Point(x, y, w * h, "Left", time.clock())
						cv2.rectangle(frameFlipped, (x,y), (x+w, y+h), (0, 0, 255), 2)
				else:
					#Checks for flipped face profiles (classifier only check one orientation)
					grayFlipped = cv2.flip(gray, 1)
					faces_profile_flipped = face_cascade_profile.detectMultiScale(grayFlipped, 1.3, 5)
					width, height = grayFlipped.shape[:2]

					for (x, y, w, h) in faces_profile_flipped:
						if(w * h > largestFace.Size):
							largestFace = Point(width - x, y, w * h, "Right", time.clock())
						cv2.rectangle(frameFlipped, (width - x,y), (width - x+w, y+h), (0, 0, 255), 2)
			if largestFace.Pose == "":
				largestFace = Point(0, 0, 0, "", time.clock())

			pointsTracking.append(largestFace)
			pointsTracking = trimList(pointsTracking)

			guestureDetected = checkGuesture(pointsTracking)  
			if guestureDetected == "Left Detected":
				return HttpResponse("Left")
			elif guestureDetected == "Right Detected":
				return HttpResponse("Right")
			
			#if space is pressed
			if key == 32:
				return HttpResponse("")
				cap.release
				cv2.destroyAllWindows

			cv2.imshow('Frame', frameFlipped)
			cv2.waitKey(30)

	cap.release
	cv2.destroyAllWindows
