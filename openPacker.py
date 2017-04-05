import sys
import json
from PIL import Image


names = sys.argv[1:]
#names = ['iso_imgs/cinema.png', 'iso_imgs/green.png', 'iso_imgs/tilenew.png']
images = map(Image.open, names)
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGBA', (total_width, max_height))

x_offset = 0
framesJson = []
for index, im in enumerate(images):
  new_im.paste(im, (x_offset, 0))
  x_offset += im.size[0]
  f = {}
  f["filename"] = names[index]
  f["frame"] = {}
  f["frame"]["x"] = x_offset
  f["frame"]["y"] = 0
  f["frame"]["w"] = im.width
  f["frame"]["h"] = im.height
  framesJson.append(f)

new_im.save('spritesheet.png')
f = open("out.json", 'w')
f.write(json.dumps(framesJson, indent = 4))
f.close()




'''
{"frames":[
	{
	"filename": "filename",
	"frame" : {"x":261,"y":1,"w":128,"h":64}
	}
]
}
'''
