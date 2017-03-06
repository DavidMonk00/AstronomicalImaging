from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

class Image:
    def __init__(self, cutoff):
        self.cutoff = cutoff
    def readImage(self):
        f = fits.open("./A1_mosaic.fits")
        self.data = f[0].data
    def generateMask(self):
        self.mask = np.zeros(self.data.shape, dtype=bool)
        self.mask[100:-100,100:-100] = True
        print np.mean(self.mask)
    def plotMask(self):
        plt.imshow(self.mask, origin='lower', interpolation='nearest',cmap='hot')
        plt.show()
    def plotImage(self):
        plt.imshow((self.data & self.mask)*self.data, origin='lower', interpolation='nearest',cmap='hot')
        plt.show()

def hist(data):
    #bins = np.arange(3300,3700+1,1)
    bins = np.arange(min(data),max(data)+1,100)
    dat = np.histogram(data,bins)
    dat = dat[0]/float(len(data))
    #print len(bins)
    #print len(dat)
    plt.plot(bins[1:],dat)
    plt.yscale('log')
    plt.show()

def main():
    image = Image(3425)
    image.readImage()
    image.generateMask()
    #image.plotMask()
    image.plotImage()

if (__name__ == '__main__'):
    main()
