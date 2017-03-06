#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <CCfits/CCfits>
#include <cmath>
#include <stdio.h>
#include "structs.h"

using namespace CCfits;

class Rect {
private:
   int top, bottom, left, right;
public:
   Rect(int l, int r, int t, int b) {
      left = l;
      right = r;
      top = t;
      bottom = b;
   }
   bool inRect(Index index) {
      return (index.x < bottom && index.x > top) && (index.y < right && index.y > left);
   }
   void maskRect(bool** mask) {
      for (int i = top; i < bottom; i++) {
         for (int j = left; j < right; j++) {
            mask[i][j] = false;
         }
      }
   }
   printRect() {
      
   }
};

class Image {
private:
   unsigned long** data;
   std::valarray<unsigned long> contents;
   bool** mask;
   long ax0,ax1;
   unsigned int cutoff;
   std::vector<Rect*> sources;
public:
   Image(int co) {
      cutoff = co;
   }
   void readImage() {
      std::auto_ptr<FITS> pInfile(new FITS("./A1_mosaic.fits",Read,true));
      PHDU& image = pInfile->pHDU();
      image.readAllKeys();
      image.read(contents);
      ax0 = image.axis(0);
      ax1 = image.axis(1);
      data = new unsigned long*[ax0];
      for (int i = 0; i < ax0; i++) {
         data[i] = new unsigned long[ax1];
      }
      for (int i = 0; i < ax0; i++) {
         for (int j = 0; j < ax1; j++) {
            data[i][j] = contents[ax0*i + j];
         }
      }
   }
   void generateMask(unsigned int min_cutoff) {
      int t = 0;
      mask = new bool*[ax0];
      for (int i = 0; i < ax0; i++) {
         mask[i] = new bool[ax1];
         for (int j = 0; j < ax1; j++) {
            if (data[i][j] < min_cutoff) {
               mask[i][j] = false;
            } else if (data[i][j] == 3421) {
               mask[i][j] = false;
            } else {
               t++;
               mask[i][j] = true;
            }
         }
      }
      std::cout << t << std::endl;
   }
   void printData() {
      for (long j = 0; j < ax1; j++) {
         std::ostream_iterator<short> c(std::cout, "\t");
         std::copy(&contents[j*ax0], &contents[(j+1)*ax0-1], c);
         std::cout << '\n';
      }
      std::cout << std::endl;
   }
   Index* maxIndex() {
   	int i,j;
   	Index* index = new Index;
   	unsigned int max = 0;
   	for (i = 0; i < ax0; i++) {
   		for(j = 0; j < ax1; j++) {
            if (mask[i][j]) {
               if (data[i][j] > max) {
      				max = data[i][j];
      				index->x = i;
      				index->y = j;
      			}
            }
   		}
   	}
      std::cout << index->x << " " << index->y << " " << max << std::endl;
   	return index;
   }
   Rect* findSourceRect(Index* centre) {
      int cx = centre->x;
      int cy = centre->y;
      int l = cy;
      int r = cy;
      int t = cx;
      int b = cx;
      while (mask[cx][l] && data[cx][l] > cutoff && r < ax0) {
         r++;
      }
      while (mask[cx][r] && data[cx][r] > cutoff && l > 0) {
         l--;
      }
      while (mask[b][cy] && data[b][cy] > cutoff && b < ax1) {
         b++;
      }
      while (mask[t][cy] && data[t][cy] > cutoff && t > 0) {
         t--;
      }
      Rect* rect = new Rect(l,r,t,b);
      return rect;
   }
   void findSources() {
      int n = 0;
      while(true) {
         Index* centre = maxIndex();
         if (!centre->x && !centre->y) {
            break;
         }
         n++;
         Rect* rect = findSourceRect(centre);
         sources.push_back(rect);
         rect->maskRect(mask);
      }
      std::cout << n << std::endl;
   }
};

int main() {
   ::Image img = ::Image(3435);
   img.readImage();
   img.generateMask(3200);
   img.findSources();
}
