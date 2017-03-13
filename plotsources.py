import numpy as np
import matplotlib.pyplot as plt
import sys, os
from log_bin_CN_2016 import log_bin

def hist(data,i):
    #bins = np.arange(3300,3700+1,1)
    bins = np.arange(min(data),max(data)+1,100)
    dat = np.histogram(data,bins)
    dat = dat[0]/float(len(data))
    #print len(bins)
    #print len(dat)
    plt.plot(bins[1:],dat,label="Cutoff = %d"%(3500+100*i))
    plt.ylim(1e-4,1e-0)
    plt.yscale('log')
    plt.xscale('log')

def plotSources(data, a):
    grid = np.zeros((4411, 2370))
    for i in range(data.shape[0]):
        x = data[i,1]
        y = data[i,0]
        grid[x-a/2:x+a/2,y-a/2:y+a/2] = data[i,2]
    plt.imshow(grid, origin='lower', interpolation='nearest',cmap='hot')
    plt.show()

def logHist(data,i):
    bins,dat = log_bin(data,a=1.75)
    plt.plot(bins,dat*len(data), label="Cutoff = %d"%(3500+100*i))
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(1e-4, 1e2)
    plt.xlabel(r'Flux (counts)')
    plt.ylabel(r'Probability Density')

def main():
    a = int(sys.argv[1])
    f = [file for file in os.listdir("./data/") if (file.find('_'+str(a)+'_') != -1)]
    f.sort()
    for i in range(len(f)):
        sources = np.genfromtxt('./data/' + f[i], delimiter=',',dtype=int)
        print len(sources)
        #plotSources(sources, a)
        logHist(sources[:,2]-min(sources[:,2]),i)
    plt.legend(loc=0)
    plt.show()

if (__name__=="__main__"):
    main()
