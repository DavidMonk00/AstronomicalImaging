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
    def __init__(self,d,f,c):
        self.cutoff = c
        print "Loading data..."
        self.radius = d/2
        self.f = fits.open("./img/A1_mosaic.fits")
        self.raw_data = self.f[0].data
        self.data = self.raw_data#[100:-100,100:-100]
        temp = np.genfromtxt('./data/'+f, delimiter=',',dtype=int)
        self.sources = np.zeros((temp.shape[0], temp.shape[1] + 1),dtype=int)
        self.sources[:,:temp.shape[1]] = temp

    def getCircleMask(self, grid, radius):
        n = grid.shape
        a = n[0]/2
        b = n[1]/2
        y,x = np.ogrid[-a:n[0]-a, -b:n[1]-b]
        mask = np.array(x*x,dtype='float64')/(radius[0]*radius[0]) + np.array(y*y,dtype='float64')/(radius[1]*radius[1]) <= 1
        grid[mask] = True
        return grid
    def getFluxSource(self, source, radius, background):
        x = source[0]
        y = source[1]
        grid = np.zeros((int(2*radius[0])+1,int(2*radius[1])+1),dtype=bool)
        grid = self.getCircleMask(grid, radius)
        data = self.data[x-radius[0]:x+radius[0]+1,y-radius[1]:y+radius[1]+1]
        flux = np.sum(np.logical_and(data,grid)*(data-background))
        #print np.array(np.logical_and(data,grid)*(data-background),dtype=int)
        #print flux
        return flux
    def getMeanCircle(self, source, radius, border):
        R = radius + border
        x = source[0]
        y = source[1]
        grid_t = np.zeros((int(2*R[0])+1,int(2*R[1])+1),dtype=bool)
        grid_t = self.getCircleMask(grid_t,R)
        data_t = self.data[x-R[0]:x+R[0]+1,y-R[1]:y+R[1]+1]
        grid_r = np.zeros((int(2*R[0])+1,int(2*R[1])+1),dtype=bool)
        grid_r = self.getCircleMask(grid_r, radius)
        grid = np.logical_xor(grid_t,grid_r)
        #print np.sum(grid*data_t)/np.sum(grid)
        d = grid*data_t
        minimum =  np.min(d[np.nonzero(d)])
        median = np.median(d[np.nonzero(d)])
        mean = np.sum(grid*data_t)/np.sum(grid)
        #print minimum, median, mean
        return minimum
    def getFlux(self):
        for i in self.sources:
            i[0] += 100
            i[1] += 100
            background = self.getMeanCircle(i,np.array((i[2],i[3])), 5)
            flux = self.getFluxSource(i,np.array((i[2],i[3])), background)
            if (flux < 0):
                i[4] = 0
            else:
                i[4] = flux
            #print background, flux
    def checkEdges(self,x,y):
        border = 2*self.radius + 1
        h = []
        v = []
        for i in range(x - border,x + border):
            for j in range(y - border, y + border):
                if np.any(np.all([i,j]==self.sources[:,:2],axis=1)):
                    v.append(i)
                    h.append(j)
                    self.sources = np.delete(self.sources,np.where(self.sources[:,:2]==[i,j])[0],0)
        #print h,v
        return (np.mean(v),np.mean(h),(float(np.ptp(v))+2*self.radius)/2,(float(np.ptp(h))+2*self.radius)/2)
    def findExtendedSources(self):
        N = len(self.sources)
        i = 0
        print "Total initial sources: %d"%(len(self.sources))
        sources = [] #[x,y,a,b]
        while (len(self.sources) > 0):
            g = self.checkEdges(self.sources[i,0],self.sources[i,1])
            #print np.sqrt(g[2]**2 + g[3]**2)
            sources.append(g)
        temp = np.array(sources)
        self.sources = np.zeros((temp.shape[0],temp.shape[1]+1))
        self.sources[:,:temp.shape[1]] = temp
        np.savetxt("./data/sources_%d_%d.csv"%(2*self.radius,self.cutoff), self.sources)
        print "Total sources: %d"%(len(self.sources))
    def getMagnitudes(self):
        self.magnitudes = []
        ZP = self.f[0].header['MAGZPT']
        for i in self.sources:
            if (i[4] > 0):
                m = ZP - 2.5*np.log10(i[4])
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
    plt.ylim(1e0,1e4)
    plt.xlim(9,20)
    plt.yscale('log')
    print bins
    print dat
    print d
    #plt.xscale('log')

def logHist(data, i):
    bins,dat = log_bin(data,a=1.5)
    plt.plot(bins,dat, label = 'Cutoff = %d'%(3500+i*100))
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(1e-7,1e-0)
    plt.xlim(1e0,1e10)

def main():
    a = int(sys.argv[1])
    c = int(sys.argv[2])
    f = [file for file in os.listdir("./data/") if (file.find('_'+str(a)+'_'+str(c)) != -1)]
    f.sort()
    #for i in range(len(f)):
    p = Photometry(a,f[0],c)
    print "Checking for extended sources..."
    p.findExtendedSources()
    print "Calculating flux..."
    p.getFlux()
    print "Converting to magnitudes..."
    #print p.sources
    p.getMagnitudes()
    print "Plotting..."
    hist(p.magnitudes)
    plt.show()

if (__name__ == '__main__'):
    main()
