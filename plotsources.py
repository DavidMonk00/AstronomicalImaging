import numpy as np
import matplotlib.pyplot as plt

def hist(data):
    #bins = np.arange(3300,3700+1,1)
    bins = np.arange(min(data),max(data)+1,10)
    dat = np.histogram(data,bins)
    dat = dat[0]/float(len(data))
    #print len(bins)
    #print len(dat)
    plt.scatter(bins[1:],dat)
    plt.ylim(0)
    #plt.yscale('log')
    #plt.show()

def plotSources(data):
    a = 24
    grid = np.zeros((4411, 2370))
    for i in range(data.shape[0]):
        x = data[i,1]
        y = data[i,0]
        grid[x-a/2:x+a/2,y-a/2:y+a/2] = data[i,2]
    plt.imshow(grid, origin='lower', interpolation='nearest',cmap='hot')
    plt.show()


def main():
    sources = np.genfromtxt('./sources.csv', delimiter=',',dtype=int)
    #plotSources(sources)
    hist(sources[:,2])

if (__name__=="__main__"):
    main()
