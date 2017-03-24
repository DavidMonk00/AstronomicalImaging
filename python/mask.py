from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from log_bin_CN_2016 import log_bin

class Rect:
    def __init__(self, lt, rb):
        self.top = lt[1]
        self.left = lt[0]
        self.bottom = rb[1]
        self.right = rb[0]
    def generateMaskRect(self,mask):
        for i in range(self.left,self.right):
            for j in range(self.bottom, self.top):
                mask[j][i] = False
        return mask

class Image:
    sources = []
    def __init__(self, cutoff):
        self.cutoff = cutoff
    def readImage(self):
        self.f = fits.open("./img/A1_mosaic.fits")
        self.raw_data = self.f[0].data
    def generateMask(self):
        self.mask = np.zeros(self.raw_data.shape, dtype=bool)
        self.mask[100:-100,100:-100] = True
    def maskRect(self, rect):
        self.mask = rect.generateMaskRect(self.mask)
    def maskStars(self):
        for i in stars:
            self.maskRect(i)
        self.data = np.logical_and(self.raw_data, self.mask) * self.raw_data
    def maskAndSave(self):
        self.generateMask()
        self.maskStars()
        self.data = self.data[100:-100,100:-100]
        self.f[0].data = self.data
        #print self.data.shape
        self.f.writeto("./img/A1_mosaic_mask.fits", overwrite=True)
    def plotMask(self):
        plt.imshow(self.mask, origin='lower', interpolation='nearest',cmap='hot')
        plt.show()
    def plotImage(self):
        image = self.data
        plt.imshow(image, origin='lower', interpolation='nearest',cmap='hot')
        plt.show()

stars = [Rect((1250,3360),(1680,3000)),
         Rect((1415,4550),(1470,0)),
         Rect((1300,160),(1550,100)),
         Rect((750,3425),(800,3200)),
         Rect((2115,3800),(2150,3700)),
         Rect((950,2840),(990,2700)),
         Rect((880,2360),(930,2220)),
         Rect((2115,2340),(2150,2280)),
         Rect((2450,3450),(2475,3380)),
         Rect((1080,470),(1640,420)),
         Rect((1010,360),(1700,305)),
         Rect((1375,260),(1480,200)),
         Rect((545,4120),(563,4080)),
         Rect((2070,1460),(2105,1400))]

def hist(data):
    #bins = np.arange(3300,3700+1,1)
    #print max(data), min(data)
    #print data
    data = data.flatten()
    bins = np.arange(3300,3550+1,1)
    #bins = np.arange(int(min(data)),max(data)+1,100)
    dat = np.histogram(data,bins)
    dat = dat[0]
    d = []
    for i in range(len(dat)):
        d.append(sum(dat[:i]))
    #print len(bins)
    #print len(dat)
    plt.errorbar(bins[1:],dat,yerr=1/np.sqrt(d),fmt='o')
    plt.ylim(0,4e5)
    d = np.zeros((len(dat),2))
    d[:,0] = bins[1:]
    d[:,1] = dat
    np.savetxt("background",d)
    #plt.xlim(9,20)
    #plt.yscale('log')
    #print bins
    #print dat
    #print d
    #plt.xscale('log')

def main():
    image = Image(3425)
    image.readImage()
    image.maskAndSave()
    hist(image.raw_data)
    #plt.show()
    #image.plotImage()

if (__name__ == '__main__'):
    main()
