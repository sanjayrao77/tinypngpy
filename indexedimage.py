
import tinypng

class PaletteBuilder():
	def __init__(self,image):
		self.rgbas={}
		self.buildpalette(image)
	def addrgba(self,rgba):
		v=self.rgbas.get(rgba,0)
		self.rgbas[rgba]=v+1
	def makelist(self):
		alphas=[]
		betas=[]
		for rgba in self.rgbas:
			if rgba[3]==255: betas.append(rgba)
			else: alphas.append(rgba)
		alphas.sort()
		betas.sort()
		full=alphas+betas
		self.list=full
	def buildpalette(self,image):
		for j in range(image.height):
			for i in range(image.width):
				rgba=image.getpixel(i,j)
				self.addrgba(rgba)
		self.makelist()
			
class IndexedImage():
	def __init__(self,image):
		self.width=image.width
		self.height=image.height
		pb=PaletteBuilder(image)
		self.colors=pb.list
		self.colorlookup={}
		self.palette=bytearray()
		self.transtable=bytearray()
		for i,c in enumerate(self.colors):
			self.colorlookup[c]=i
			self.palette.extend(c[0:3])
			if c[3]!=255:
				if len(self.transtable)!=i: self.transtable+=[255]*(i-len(self.transtable))
				self.transtable.append(c[3])
		if not len(self.transtable): self.transtable=None
		count=len(self.colors)
		if count<=4:
			self.ppb=4
			self.stride=int((self.width+3)/4)
		elif count<=16:
			self.ppb=2
			self.stride=int((self.width+1)/2)
		elif count<=256:
			self.ppb=1
			self.stride=self.width
		else: raise ValueError
		self.rows=[]
		for i in range(self.height): self.rows.append([0]*self.stride)
		self.getpixels(image)
	def getpixels(self,image):
		colorlookup=self.colorlookup
		if self.ppb==1:
			for j in range(image.height):
				for i in range(image.width):
					self.rows[j][i]=colorlookup[image.getpixel(i,j)]
		elif self.ppb==2:
			for j in range(image.height):
				id2=0
				for i in range(0,image.width-1,2):
					c1=colorlookup[image.getpixel(i,j)]
					c2=colorlookup[image.getpixel(i+1,j)]
					self.rows[j][id2]=(c1<<4)|c2
					id2+=1
				i+=2
				if i<image.width:
					c1=colorlookup[image.getpixel(i,j)]
					self.rows[j][id2]=(c1<<4)
		elif self.ppb==4:
			for j in range(image.height):
				id4=0
				for i in range(0,image.width-3,4):
					c1=colorlookup[image.getpixel(i,j)]
					c2=colorlookup[image.getpixel(i+1,j)]
					c3=colorlookup[image.getpixel(i+2,j)]
					c4=colorlookup[image.getpixel(i+3,j)]
					self.rows[j][id4]=(c1<<6)|(c2<<4)|(c3<<2)|c4
					id4+=1
				i+=4
				if i<image.width:
					c1=colorlookup[image.getpixel(i,j)]
					c2=colorlookup[image.getpixel(i+1,j)] if i+1<image.width else 0
					c3=colorlookup[image.getpixel(i+2,j)] if i+2<image.width else 0
					self.rows[j][id4]=(c1<<6)|(c2<<4)|(c3<<2)
	def getpng(self,isfast=False):
		return tinypng.PngCompress.create(self.width,self.height,self.rows,isfast=isfast,palette=self.palette,transtable=self.transtable)

