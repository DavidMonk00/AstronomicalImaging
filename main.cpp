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
};

class Image {
private:
   unsigned long** data;
   std::valarray<unsigned long> contents;
   bool** mask;
   long ax0,ax1;
   unsigned int cutoff;
   std::vector<Index*> sources;
public:
   Image(int co) {
      cutoff = co;
   }
   void readImage() {
      std::auto_ptr<FITS> pInfile(new FITS("./A1_mosaic_mask.fits",Read,true));
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
   void generateMask() {
      mask = new bool*[ax0];
      for (int i = 0; i < ax0; i++) {
         mask[i] = new bool[ax1];
         for (int j = 0; j < ax1; j++) {
            if (data[i][j]) {
               mask[i][j] = true;
            }
         }
      }
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
                  index->max = max;
      			}
            }
   		}
   	}
      std::cout << index->x << " " << index->y << " " << max << std::endl;
   	return index;
   }
   void findSources(int aperture) {
      int a = aperture/2;
      int n = 0;
      while(true) {
         Index* centre = maxIndex();
         int x = centre->x;
         int y = centre->y;
         if (centre->max < cutoff) {
            break;
         }
         n++;
         sources.push_back(centre);
         int i,j;
         int bottom = (x-a)>0 ? x-a : 0;
         int top = (x+a)<ax0 ? x+a : ax0;
         int left = (y-a)>0 ? y-a : 0;
         int right = (y+a)<ax1 ? y+a : ax1;
         for (i = bottom; i < top; i++){
            for (j = left; j < right; j++) {
               mask[i][j] = false;
            }
         }
      }
      std::cout << n << std::endl;
   }
};

int main() {
   ::Image img = ::Image(3700);
   img.readImage();
   img.generateMask();
   img.findSources(12);
}
