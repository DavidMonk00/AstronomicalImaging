from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

def hist(data):
    bins = np.arange(3300,3700+1,1)
    #bins = np.arange(5000,max(data)+1,100)
    dat = np.histogram(data,bins)
    dat = dat[0]/float(len(data))
    #print len(bins)
    #print len(dat)
    plt.plot(bins[1:],dat)
    #plt.yscale('log')
    plt.show()

def main():
    hdulist = fits.open("./A1_mosaic.fits")
    data = hdulist[0].data.flatten()
    #print data
    hist(data)

if (__name__ == '__main__'):
    main()
