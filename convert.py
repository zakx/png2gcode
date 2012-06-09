# encoding: utf-8
import Image
import math

im = Image.open("zakx.png").convert("L")
dimensions = im.size # (x,y)
pix = im.load()
gcode = [
	"%",
	"G21",
	"G90",
	"S255",
	"G1 F600",
	"G0 F10000",
]

def brightness(s):
	return int((255-s)/10*2.5)

def endline(x,y):
	ret = ["M5"]
	for i in xrange(x+1, x+10):
		ret.append("G01X%.3fY%.3fS0" % (i,y))
	return ret

for y in xrange(0, dimensions[1]):
	started = False
	#gcode.append("M3") # turn laser on
	for x in xrange(0, dimensions[0]):
		if not started:
			if brightness(pix[int(x), int(y)]) > 0:
				started = True
				gcode.append("G01X%.3fY%.3fS0" % (float(x), float(y)))
				#gcode.append("M3") # turn laser on
			else:
				continue
		gcode.append("M3") # turn laser on
		gcode.append("G01X%.3fY%.3fS%d" % (float(x), float(y), brightness(pix[int(x),int(y)])))
		gcode.append("M5") # turn laser off
	if started:
		gcode.extend(endline(x, y))
	gcode.append("M5") # turn laser off

gcode.extend([
		"S0",
		"G00X0Y0F16000",
		"%"
	]
)

for line in gcode: print line