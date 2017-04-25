import PIL
import Image
import random
import math
import noise


def generate_noise(pixels):
  for y in range(dim):
    for x in range(dim):
      v = int(255*noise.pnoise2(.1*x,.1*y))
      pixels[x, y] = (v,v,v)
      
  img.save('noise.png')
  
def generate_gradient(pixels):
  for y in range(dim):
    for x in range(dim):
      n=math.sqrt((x-dim/2.0)**2 + (y-dim/2.0)**2)/(math.sqrt(2.0)*dim/2.0)
      v = int(255*n)
      pixels[x, y] = (v,v,v)
  img.save("circle_gradient.png")

def generate_random_mask(pixels):
  for y in range(dim):
    for x in range(dim):
      pixels[x, y] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
  img.save("random_mask.png")

def generate_grid(pixels):
  for y in range(dim):
    for x in range(dim):
      if(x%16<=4 or y%16<=4):
        pixels[x, y] = (0,0,0)
      else:
        pixels[x,y] = (255,255,255)
  img.save("grid.png")


dim = 256

img = Image.new( 'RGB', (dim,dim), "red")
pixels = img.load()
generate_grid(pixels)
