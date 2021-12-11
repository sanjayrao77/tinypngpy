#!/usr/bin/python3

try:
	import tinypng
except ImportError:
	tinypng=None
try:
	import tinytinypng
except ImportError:
	tinytinypng=None
import sys

def rgba_small(isfast=False):
	if not tinypng: raise ValueError("tinypng is not loaded")
	outfilename='out.png'
	image=tinypng.FlatImage(500,500,[0,0,0,128])
	for i in range(500):
		image.setpixel(i,i,(255,0,0,255))
		image.setpixel(499-i,i,(255,255,0,255))
	print('Making png and writing to %s'%outfilename)
	b=image.getpng(isfast=isfast)
	f=open(outfilename,'wb')
	f.write(b)
	f.close()
def rgba_fast(): rgba_small(isfast=True)

def rgb_small(isfast=False):
	if not tinypng: raise ValueError("tinypng is not loaded")
	outfilename='out.png'
	image=tinypng.FlatImage(500,500,[0,0,0])
	for i in range(500):
		image.setpixel(i,i,(255,0,0))
		image.setpixel(499-i,i,(255,255,0))
	print('Making png and writing to %s'%outfilename)
	b=image.getpng(isfast=isfast)
	f=open(outfilename,'wb')
	f.write(b)
	f.close()
def rgb_fast(): rgb_small(isfast=True)

def graya_small(isfast=False):
	if not tinypng: raise ValueError("tinypng is not loaded")
	outfilename='out.png'
	image=tinypng.FlatImage(500,500,[0,128])
	for i in range(500):
		image.setpixel(i,i,(255,255))
		image.setpixel(499-i,i,(128,255))
	print('Making png and writing to %s'%outfilename)
	b=image.getpng(isfast=isfast)
	f=open(outfilename,'wb')
	f.write(b)
	f.close()
def graya_fast(): graya_small(isfast=True)

def gray_small(isfast=False):
	if not tinypng: raise ValueError("tinypng is not loaded")
	outfilename='out.png'
	image=tinypng.FlatImage(500,500,[0])
	for i in range(500):
		image.setpixel(i,i,(255,))
		image.setpixel(499-i,i,(128,))
	print('Making png and writing to %s'%outfilename)
	b=image.getpng(isfast=isfast)
	f=open(outfilename,'wb')
	f.write(b)
	f.close()
def gray_fast(): gray_small(isfast=True)

def tiny_rgba():
	if not tinytinypng: raise ValueError("tinypng is not loaded")
	outfilename='out.png'
	image=tinytinypng.FlatImage(500,500,[0,0,0,128])
	for i in range(500):
		image.setpixel(i,i,(255,0,0,255))
		image.setpixel(499-i,i,(255,255,0,255))
	print('Making png and writing to %s'%outfilename)
	b=image.getpng()
	f=open(outfilename,'wb')
	f.write(b)
	f.close()

def tiny_rgb():
	if not tinytinypng: raise ValueError("tinypng is not loaded")
	outfilename='out.png'
	image=tinytinypng.FlatImage(500,500,[0,0,0])
	for i in range(500):
		image.setpixel(i,i,(255,0,0))
		image.setpixel(499-i,i,(255,255,0))
	print('Making png and writing to %s'%outfilename)
	b=image.getpng()
	f=open(outfilename,'wb')
	f.write(b)
	f.close()

def printhelp():
	print('tinypng.py examples')
	print('Make an RGBA png (high compression): ./examples.py rgba_small')
	print('Make an RGBA png (low compression): ./examples.py rgba_fast')
	print('Make an RGB png (high compression): ./examples.py rgb_small')
	print('Make an RGB png (low compression): ./examples.py rgb_fast')
	print('Make a GRAYALPHA png (high compression): ./examples.py graya_small')
	print('Make a GRAYALPHA png (low compression): ./examples.py graya_fast')
	print('Make a GRAYSCALE png (high compression): ./examples.py gray_small')
	print('Make a GRAYSCALE png (low compression): ./examples.py gray_fast')
	print('Make an RGBA png using tinytinypng.py: ./examples.py tiny_rgba')
	print('Make an RGB png using tinytinypng.py: ./examples.py tiny_rgb')

if len(sys.argv)<2: printhelp()
for arg in sys.argv[1:]:
	if arg in globals(): globals().get(arg)()
	else: print('Unknown example',arg)
