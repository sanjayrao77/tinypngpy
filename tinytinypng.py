#!/usr/bin/python3

#  * github.com/sanjayrao77
#  * tinytinypng.py - very small code to compress pngs with decent compression
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
import zlib

class PngCompress(): # this works for 24bit RGB and 32bit RGBA
	@staticmethod
	def create(width,height,rows,isrgba=True,level=6):
		bio=io.BytesIO()
		bio.write(b'\x89PNG\r\n\x1a\n')
		colortype=6 if isrgba else 2
		PngCompress.writechunk(bio,b'IHDR',struct.pack('>2I5B',width,height,8,colortype,0,0,0))
		PngCompress.write_simple(bio,rows,level)
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

class FlatImage():
	def __init__(self,width,height,fillpixel):
		self.Bpp=len(fillpixel)
		self.width=width
		self.height=height
		self.rows=[]
		for i in range(height): self.rows.append(fillpixel*width)
	def setpixel(self,x,y,pixel):
		self.rows[y][x*self.Bpp:(x+1)*self.Bpp]=pixel
	def getpng(self):
		return PngCompress.create(self.width,self.height,self.rows,(self.Bpp==4))
