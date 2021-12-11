# tinypng.py

## Overview

This code is licensed under GPL version 2.

tinypng.py creates well-compressed png files, in python.

I needed high png compression for my pythonshp maps (on github) and
tinypng.py comes from that.

If you care more about tiny code size rather than compressed size, you could
use my tinytinypng.py (included here) at about 2k. It does decent compression
quickly but files are roughly 50% larger than ideal.

## License

This python code is licensed under the GPLv2. The GPL license text is widely available
and should be downloadable above (on github).

## Installation

You can just download tinypng.py from here, placing it in your code
directory, and import it. tinypng.py is roughly 4k, tinytiny.py is roughly 2k.

Example:
```
#!/usr/bin/python3

import tinypng

outfilename='out.png'
image=tinypng.FlatImage(500,500,[0,0,0,128])
for i in range(500):
	image.setpixel(i,i,(255,0,0,255))
	image.setpixel(499-i,i,(255,255,0,255))
print('Making png and writing to %s'%outfilename)
b=image.getpng(isfast=False)
f=open(outfilename,'wb')
f.write(b)
f.close()
```

## Examples

I've included an examples.py with 4 different image examples:
1. 32bit RGBA
2. 24bit RGB
3. 16bit Grayscale + Alpha
4. 8bit Grayscale

You can run examples.py to get a list of available examples:
```
tinypng.py examples
Make an RGBA png (high compression): ./examples.py rgba_small
Make an RGBA png (low compression): ./examples.py rgba_fast
Make an RGB png (high compression): ./examples.py rgb_small
Make an RGB png (low compression): ./examples.py rgb_fast
Make a GRAYALPHA png (high compression): ./examples.py graya_small
Make a GRAYALPHA png (low compression): ./examples.py graya_fast
Make a GRAYSCALE png (high compression): ./examples.py gray_small
Make a GRAYSCALE png (low compression): ./examples.py gray_fast
Make an RGBA png using tinytinypng.py: ./examples.py tiny_rgba
Make an RGB png using tinytinypng.py: ./examples.py tiny_rgb
```

## Performance

Using default settings, tinypng.py will create very small pngs but it takes
some time.

Sometimes speed matters more than size (e.g. when testing output) and 
tinypng.py supports "isfast=True" for those times. With isfast=True,
output is somewhat compressed but the priority is speed.
There are examples of this in examples.py.

