import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import sys

class Source:
    def __init__(x,y,flux):
        self.centre = (x,y)
        self.flux = flux

class Photometry:
    def __init__(self,d):
        self.radius = d/2
        self.f = fits.open("./A1_mosaic.fits")
        self.raw_data = self.f[0].data
        self.data = self.raw_data[100:-100,100:-100]
        self.sources = np.genfromtxt('./sources.csv', delimiter=',',dtype=int)

    def getCircleMask(self, grid, radius):
        n = grid.shape
        a = n[0]/2
        b = n[1]/2
        y,x = np.ogrid[-a:n[0]-a, -b:n[1]-b]
        mask = x*x + y*y <= radius*radius
        grid[mask] = True
        return grid
    def getFluxSource(self, source, radius, background):
        x = source[1]
        y = source[0]
        grid = np.zeros((2*radius+1,2*radius+1),dtype=bool)
        grid = self.getCircleMask(grid, radius)
        data = self.data[x-radius:x+radius+1,y-radius:y+radius+1]
        flux = np.sum(np.logical_and(data,grid)*(data-background))
        return flux
    def getMeanCircle(self, source, radius, border):
        R = radius + border
        x = source[1]
        y = source[0]
        grid_t = np.zeros((2*R+1,2*R+1),dtype=bool)
        grid_t = self.getCircleMask(grid_t, R)
        data_t = self.data[x-R:x+R+1,y-R:y+R+1]
        grid_r = np.zeros((2*R+1,2*R+1),dtype=bool)
        grid_r = self.getCircleMask(grid_r, radius)
        grid = np.logical_xor(grid_t,grid_r)
        print np.sum(grid*data_t)/np.sum(grid)
        return np.sum(grid*data_t)/np.sum(grid)
    def getFlux(self):
        sources = []
        for i in self.sources:
            background = self.getMeanCircle(i,self.radius, 5)
            flux = self.getFluxSource(i,self.radius, background)
            sources.append(flux)
        return sources

def hist(data):
    #bins = np.arange(3300,3700+1,1)
    bins = np.arange(min(data),max(data)+1,1e5)
    dat = np.histogram(data,bins)
    dat = dat[0]/float(len(data))
    #print len(bins)
    #print len(dat)
    plt.scatter(bins[1:],dat)
    plt.ylim(1e-4,1e-0)
    plt.yscale('log')
    plt.xscale('log')
    plt.show()

def main():
    p = Photometry(int(sys.argv[1]))
    p.getFlux()

if (__name__ == '__main__'):
    main()
