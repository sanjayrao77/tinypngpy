#!/usr/bin/python3

#  * github.com/sanjayrao77
#  * tinypng.py - small program to compress pngs nearly minimally
#  * Copyright (C) 2021 Sanjay Rao
#  *
#  * This program is free software; you can redistribute it and/or modify
#  * it under the terms of the GNU General Public License as published by
#  * the Free Software Foundation; either version 2 of the License, or
#  * (at your option) any later version.
#  *
#  * This program is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  * GNU General Public License for more details.
#  *
#  * You should have received a copy of the GNU General Public License
#  * along with this program; if not, write to the Free Software
#  * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import io
import struct
import sys
import zlib

isverbose_global=True

class PngCompress():
	@staticmethod
	def create(width,height,rows,isfast=False):
		bio=io.BytesIO()
		Bpp=int(len(rows[0])/width)
		if Bpp==4: colortype=6 # rgba
		elif Bpp==3: colortype=2 # rgb
		elif Bpp==2: colortype=4 # greyscale+alpha
		elif Bpp==1: colortype=0 # greyscale
		else: raise ValueError
		bio.write(b'\x89PNG\r\n\x1a\n')
		PngCompress.writechunk(bio,b'IHDR',struct.pack('>2I5B',width,height,8,colortype,0,0,0))
		if isfast: PngCompress.write_simple(bio,rows,3)
		else: PngCompress.write_small(bio,rows,width,Bpp)
		PngCompress.writechunk(bio,b'IEND',b'')
		return bio.getvalue()
	@staticmethod
	def writechunk(bio,key,value):
		bio.write(struct.pack('>I',len(value)))
		bio.write(key)
		bio.write(value)
		bio.write(struct.pack('>I',zlib.crc32(value,zlib.crc32(key))))
	@staticmethod
	def write_simple(bio,rows,complevel): # complevel, 3:fast, 6:medium, 9: smallest
		ba=bytearray()
		for row in rows:
			ba.append(0)
			ba.extend(row)
		PngCompress.writechunk(bio,b'IDAT',zlib.compress(ba,complevel))
	@staticmethod
	def paethpredictor(a,b,c): # PaethPredictor is lifted from PNG spec, presumably this is free as it's required for all readers
		# a:left, b:above, c:upperleft
		p=a+b-c
		pa=abs(p-a)
		pb=abs(p-b)
		pc=abs(p-c)
		# return nearest of a,b,c, breaking ties in order a,b,c
		if pa<=pb and pa<=pc: return a
		if pb<=pc: return b
		return c
	@staticmethod
	def getcompsize(zco,line):
		z=zco.copy()
		return len(z.compress(line))+len(z.flush())
	@staticmethod
	def write_small(bio,rows,width,Bpp):
		zco=zlib.compressobj(level=9,memLevel=9)
		zba=bytearray()
		widthxB=width*Bpp
		ba=bytearray(1+widthxB)
		tba=bytearray(1+widthxB)
		urow=[0]*widthxB
		for row in rows:
			ba[0]=0
			ba[1:]=row
			bal=PngCompress.getcompsize(zco,ba)
			if True:
				tba[0]=1 # Left
				tba[1:1+Bpp]=row[0:Bpp]
				for i in range(Bpp,widthxB): tba[i+1]=(row[i]-row[i-Bpp])%256
				tbal=PngCompress.getcompsize(zco,tba)
				if tbal<bal: ba,tba,bal=(tba,ba,tbal)
			if True:
				tba[0]=2 # Up
				for i in range(widthxB): tba[i+1]=(row[i]-urow[i])%256
				tbal=PngCompress.getcompsize(zco,tba)
				if tbal<bal: ba,tba,bal=(tba,ba,tbal)
			if True:
				tba[0]=3 # Left + Up
				for i in range(Bpp): tba[i+1]=(row[i]-(urow[i]>>1))%256
				for i in range(Bpp,widthxB): tba[i+1]=(row[i]-((row[i-Bpp]+urow[i])>>1))%256
				tbal=PngCompress.getcompsize(zco,tba)
				if tbal<bal: ba,tba,bal=(tba,ba,tbal)
			if True:
				tba[0]=4 # Paeth
				for i in range(Bpp): tba[i+1]=(row[i]-PngCompress.paethpredictor(0,urow[i],0))%256
				for i in range(Bpp,widthxB): tba[i+1]=(row[i]-PngCompress.paethpredictor(row[i-Bpp],urow[i],urow[i-Bpp]))%256
				tbal=PngCompress.getcompsize(zco,tba)
				if tbal<bal: ba,tba,bal=(tba,ba,tbal)
			zba.extend(zco.compress(ba))
			urow=row
		zba.extend(zco.flush())
		PngCompress.writechunk(bio,b'IDAT',zba)

class FlatImage():
	def __init__(self,width,height,fillpixel):
		self.Bpp=len(fillpixel)
		self.width=width
		self.height=height
		self.rows=[]
		for i in range(height): self.rows.append(fillpixel*width)
	def setpixel(self,x,y,pixel):
		self.rows[y][x*self.Bpp:(x+1)*self.Bpp]=pixel
	def getpng(self,isfast=False):
		return PngCompress.create(self.width,self.height,self.rows,isfast)
