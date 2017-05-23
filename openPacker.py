import sys
import json
from PIL import Image
import random

class ImageData():

	def __init__(self, name, im, w, h):
		self._name = name
		self._image = im
		self._width = w
		self._height = h
		self._area = w*h

	def setX(self, x):
		self._x = x

	def setY(self, y):
		self._y = y

	def getX(self):
		return self._x

	def getY(self):
		return self._y

	def getName(self):
		return self._name

	def getImage(self):
		return self._image

	def getWidth(self):
		return self._width

	def getHeight(self):
		return self._height

	def getArea(self):
		return self._area

class Point():
	def __init__ (self, x, y, valid=True):
		self.x = x
		self.y = y
		self. valid = valid

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __hash__(self):
		return hash((self.x, self.y))

	def __str__(self):
		return "("+str(self.x)+","+str(self.y)+") " + ("valid" if self.valid else "invalid")

def loadImages(names):

	images = []
	totalWidth = 0
	maxHeight = 0

	for name in names:
		im = Image.open(name)
		images.append(ImageData(name, im, im.width, im.height))
		totalWidth += im.width
		maxHeight = max(maxHeight, im.height)

	return (images, totalWidth, maxHeight)


def generateAtlas(imageData):

	images = imageData[0]
	images.sort(key=lambda x: x.getHeight(), reverse=True)
	images[0].setX(0)
	images[0].setY(0)

	totalWidth = imageData[1]
	maxHeight = images[0].getHeight()

	x_offset = images[0].getWidth()
	y_offset = 0
	curWidth = 0
	curHeight = maxHeight
	pointsToCheck = []

	for im in images[1:]:

		placed = False

		for p in pointsToCheck:
			x = p.x
			y = p.y
			stillValid = p.valid

			if (stillValid and (y + im.getHeight() < curHeight)):
				im.setX(x)
				im.setY(y)
				p.valid = False
				placed = True
				curWidth = max(curWidth, im.getX() + im.getWidth())
				newPoint = Point(im.getX(), im.getY() + im.getHeight())
				if ( not(newPoint in pointsToCheck) ):
					pointsToCheck.append(newPoint)
				break # break is important as the exactly above line adds more points so we get into an infinite loop
			elif (stillValid and (x + im.getWidth() < curWidth)):
				im.setX(x)
				im.setY(y)
				p.valid = False
				placed = True
				curHeight = max(curHeight, im.getY() + im.getHeight())
				newPoint = Point(im.getX(), im.getY() + im.getHeight())
				if ( not(newPoint in pointsToCheck) ):
					pointsToCheck.append(newPoint)
				break # break is important as the exactly above line adds more points so we get into an infinite loop


		if placed == False:
			im.setX(x_offset)
			im.setY(y_offset)
			newPoint = Point(im.getX(), im.getY() + im.getHeight())
			if (not (newPoint in pointsToCheck)):
			    pointsToCheck.append(newPoint)
			x_offset += im.getWidth()
			curWidth += im.getWidth()



	newImage = Image.new('RGBA', (curWidth, curHeight))
	for im in images:
		newImage.paste(im.getImage(), (im.getX(), im.getY()))

	return newImage


def export(images, newImage):

	# write the image
	newImage.save('spritesheet.png')

	# make JSON
	framesJson = []
	for im in images[0]:
	  f = {}
	  f["filename"] = im.getName()
	  f["frame"] = {}
	  f["frame"]["x"] = im.getX()
	  f["frame"]["y"] = im.getY()
	  f["frame"]["w"] = im.getWidth()
	  f["frame"]["h"] = im.getHeight()
	  framesJson.append(f)

	f = open("out.json", 'w')
	f.write(json.dumps(framesJson, indent = 4))
	f.close()


def main():

	names = sys.argv[1:]
	#names = ['iso_imgs/cinema.png', 'iso_imgs/green.png', 'iso_imgs/tilenew.png']
	images = loadImages(names)
	newImage = generateAtlas(images)
	export(images, newImage)


if __name__ == '__main__':
	main()
