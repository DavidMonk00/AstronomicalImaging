import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import sys, os
from log_bin_CN_2016 import log_bin

class Source:
    def __init__(x,y,flux):
        self.centre = (x,y)
        self.flux = flux

class Photometry:
    def __init__(self,d,f):
        self.radius = d/2
        self.f = fits.open("./A1_mosaic.fits")
        self.raw_data = self.f[0].data
        self.data = self.raw_data#[100:-100,100:-100]
        self.sources = np.genfromtxt('./data/'+f, delimiter=',',dtype=int)

    def getCircleMask(self, grid, radius):
        n = grid.shape
        a = n[0]/2
        b = n[1]/2
        y,x = np.ogrid[-a:n[0]-a, -b:n[1]-b]
        mask = x*x + y*y <= radius*radius
        grid[mask] = True
        return grid
    def getFluxSource(self, source, radius, background):
        x = source[0]
        y = source[1]
        grid = np.zeros((2*radius+1,2*radius+1),dtype=bool)
        grid = self.getCircleMask(grid, radius)
        data = self.data[x-radius:x+radius+1,y-radius:y+radius+1]
        flux = np.sum(np.logical_and(data,grid)*(data-background))
        #print np.array(np.logical_and(data,grid)*(data-background),dtype=int)
        #print flux
        return flux
    def getMeanCircle(self, source, radius, border):
        R = radius + border
        x = source[0]
        y = source[1]
        grid_t = np.zeros((2*R+1,2*R+1),dtype=bool)
        grid_t = self.getCircleMask(grid_t, R)
        data_t = self.data[x-R:x+R+1,y-R:y+R+1]
        grid_r = np.zeros((2*R+1,2*R+1),dtype=bool)
        grid_r = self.getCircleMask(grid_r, radius)
        grid = np.logical_xor(grid_t,grid_r)
        #print np.sum(grid*data_t)/np.sum(grid)
        return np.sum(grid*data_t)/np.sum(grid)
    def getFlux(self):
        sources = []
        s = 0
        for i in self.sources:
            i[0] += 100
            i[1] += 100
            background = self.getMeanCircle(i,self.radius, 3)
            flux = self.getFluxSource(i,self.radius, background)
            if (flux < 0):
                s += 1
            #print background, flux
            sources.append(flux)
        print s
        return sources
    def getMagnitudes(self):
        ZP = self.f[0].header['MAGZPT']
        self.magnitudes = []
        sources = [i for i in self.getFlux() if (i > 0)]
        for i in sources:
            m = ZP - 2.5*np.log10(i)
            #print m
            self.magnitudes.append(m)

def hist(data):
    #bins = np.arange(3300,3700+1,1)
    #print max(data), min(data)
    #print data
    bins = np.arange(int(min(data)),max(data)+1,0.5)
    dat = np.histogram(data,bins)
    dat = dat[0]
    d = []
    for i in range(len(dat)):
        d.append(sum(dat[:i]))
    #print len(bins)
    #print len(dat)
    plt.errorbar(bins[1:],d,yerr=1/np.sqrt(d),fmt='o')
    plt.ylim(1e-1,1e4)
    plt.xlim(9,25.5)
    plt.yscale('log')
    print bins
    print dat
    #plt.xscale('log')

def logHist(data, i):
    bins,dat = log_bin(data,a=2)
    plt.plot(bins,dat, label = 'Cutoff = %d'%(3500+i*100))
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(1e-7,1e-0)
    plt.xlim(1e0,1e10)

def main():
    a = int(sys.argv[1])
    f = [file for file in os.listdir("./data/") if (file.find('_'+str(a)+'_') != -1)]
    f.sort()
    #for i in range(len(f)):
    p = Photometry(a,f[0])
    #p.getMagnitudes()
    #hist(p.getFlux())
    p.getMagnitudes()
    hist(p.magnitudes)
        #logHist(p.getFlux(), i)
    #plt.legend(loc=0)
    plt.show()

if (__name__ == '__main__'):
    main()
