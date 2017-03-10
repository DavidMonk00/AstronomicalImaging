import numpy as np

def drawcircle(grid,x0, y0, radius):
    x = radius;
    y = 0
    err = 0;
    while (x >= y):
        grid[x0 + x, y0 + y] = 8
        grid[x0 + y, y0 + x] = 8
        grid[x0 - y, y0 + x] = 8
        grid[x0 - x, y0 + y] = 8
        grid[x0 - x, y0 - y] = 8
        grid[x0 - y, y0 - x] = 8
        grid[x0 + y, y0 - x] = 8
        grid[x0 + x, y0 - y] = 8
        if (err <= 0):
            y += 1
            err += 2*y + 1
        if (err > 0):
            x -= 1
            err -= 2*x + 1
    return grid

grid = np.ones((30,30),dtype=int)
#for i in range(1,15):
#    grid = drawcircle(grid, 14,14,i)
a, b = 14, 14
n = 30
r = 10

y,x = np.ogrid[-a:n-a, -b:n-b]
mask = x*x + y*y <= r*r

grid = np.ones((n, n),dtype=int)
grid[mask] = 8
print grid
