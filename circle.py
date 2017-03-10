import numpy as np

def getCircleMask(a,b, radius, grid):
    n = grid.shape
    y,x = np.ogrid[-a:n[0]-a, -b:n[1]-b]
    mask = x*x + y*y <= radius*radius
    grid[mask] = True
    return grid

grid = np.zeros((31, 31),dtype=bool)
grid = getCircleMask(15,15,15,grid)
print np.array(grid,dtype=int)
