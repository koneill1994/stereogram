# stereogram test

import PIL
import Image
import random
import math


'''
left_view  = [[(0,0,0) for x in range(dim)] for y in range(dim)]
right_view = [[(0,0,0) for x in range(dim)] for y in range(dim)]

points = []
'''

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

def AddDisparityMap(disparity_map, depth_px):
  for y in range(depth_map.size[1]): #height
    for x in range(depth_map.size[0]): #width
      z=int(list_average(depth_pixels[x,y])*depth/255)
      #print z
      if(x-z>0 and x+z<width):
        disparity_map[y][(x-z)%width]-=z
        disparity_map[y][(x+z)%width]+=z
        
  return disparity_map

def display_disparity_map(disparity_map):
  im = Image.new( 'RGB', (len(disparity_map),len(disparity_map[0])), "red")
  px = im.load()
  
  for x in range(len(disparity_map)):
    for y in range(len(disparity_map[0])):
      v=(127+255*disparity_map[y][x]/depth)%255
      px[x,y]=(v,v,v)
  im.save('disparity_map.png')

n_points=1000
depth=100
dot_size=5

depth_map=Image.open("circle_gradient.png")
depth_pixels=depth_map.load()

background=Image.open("noise2.png")
bg_px=background.load()

dim = depth_map.size[0] # length of a single image on a side

height = dim
width = dim

disparity_map = [[0 for x in range(dim)] for y in range(dim)]


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

'''
for y in range(depth_map.size[1]): #height
  for x in range(depth_map.size[0]): #width
    z=int(list_average(depth_pixels[x,y])*depth)
    col=bg_px[x%background.size[0],y%background.size[1]]
    left_view[y][x]=bg_px[(x-z)%background.size[0],y%background.size[1]]
    right_view[y][x]=bg_px[(x+z)%background.size[0],y%background.size[1]]
'''

'''
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
'''


img = Image.new( 'RGB', (width,height), "red")
pixels = img.load()

disparity_map = AddDisparityMap(disparity_map, depth_pixels)
display_disparity_map(disparity_map)

#print disparity_map

for y in range(depth_map.size[1]): #height
  for x in range(depth_map.size[0]): #width
    x_offset = disparity_map[y][x]
    pixels[x, y] = bg_px[(x+x_offset)%background.size[0], y%background.size[1]]

img.save("test.png")

