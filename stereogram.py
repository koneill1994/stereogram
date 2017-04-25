# stereogram test

import PIL
import Image
import random
import math

dim = 1024 # length of a single image on a side

height = dim
width = 2*dim

left_view  = [[(0,0,0) for x in range(dim)] for y in range(dim)]
right_view = [[(0,0,0) for x in range(dim)] for y in range(dim)]

points = []

def list_average(l):
  s=0
  for i in l:
    s+=i
  return 1.0*s/len(l)

def GenerateRandom3dPoint(dim,depth,depth_pixels):
  # x, y, z, color
  x=random.randint(0,dim-1)
  y=random.randint(0,dim-1)
  if(y<dim/2.0):
    z=int(1.0*depth/2)
  else:
    z=int(1.0*y/dim*depth)
  z=int(list_average(depth_pixels[x,y])*depth)
  col=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
  return (x,y,z,col)

def AddPointsWithDisparity(direction,p,view):
  coords=[p[0]+p[2]*direction,p[1]]
  for c in coords:
    if(c<0 or c>=dim): return view
  view[coords[1]][coords[0]]=p[3]
  return view

def dist((x,y),(a,b)):
  return math.sqrt((x-a)**2+(y-b)**2)

def AddFocusCues(pos,col):
  cues = [(dim/2,0),(3*dim/2,0)]
  for c in cues:
    if(dist(pos,c)<32):
      return (255,0,0)
  return col

n_points=1000
depth=20
dot_size=5

depth_map=Image.open("landscape.png")
depth_pixels=depth_map.load()

background=Image.open("noise.png")
bg_px=background.load()
'''
# generate points
for i in range(0,n_points):
  point=GenerateRandom3dPoint(dim,depth,depth_pixels)
  for x in range(0,dot_size):
    for y in range(0,dot_size):
      points.append([point[0]+x,point[1]+y,point[2],point[3]])


# add points
for p in points:
  left_view = AddPointsWithDisparity(-1,p,left_view)
  right_view = AddPointsWithDisparity(1,p,right_view)
'''


for y in range(depth_map.size[1]): #height
  for x in range(depth_map.size[0]): #width
    z=int(list_average(depth_pixels[x,y])*depth)
    col=bg_px[x%background.size[0],y%background.size[1]]
    left_view[y][x]=bg_px[(x-z)%background.size[0],y%background.size[1]]
    right_view[y][x]=bg_px[(x+z)%background.size[0],y%background.size[1]]

# draw image
img = Image.new( 'RGB', (width,height), "red")
pixels = img.load()

for y in range(height):
  for x in range(width):
    if(x<dim):
      pixels[x, y] = left_view[y][x]
    else:
      pixels[x, y] = right_view[y][x-dim]
    pixels[x, y] = AddFocusCues((x,y),pixels[x,y])

img.save("test.png")







