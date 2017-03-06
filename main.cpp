#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <CCfits/CCfits>
#include <cmath>

using namespace CCfits;

struct Index {
   int x;
   int y;
};

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
      for (int i = left; i < right; i++) {
         for (int j = top; j < bottom; j++) {
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
   	return index;
   }
   Rect* findSourceRect() {
      Index* centre = maxIndex();
      int cx = centre->x;
      int cy = centre->y;
      int l = cx;
      int r = cx;
      int t = cy;
      int b = cy;
      while (mask[r][cy] && data[r][cy] > cutoff) {
         r++;
      }
      while (mask[l][cy] && data[l][cy] > cutoff) {
         l--;
      }
      while (mask[cx][b] && data[cx][b] > cutoff) {
         b++;
      }
      while (mask[cx][t] && data[cx][t] > cutoff) {
         t--;
      }
      Rect* rect = new Rect(l,r,t,b);
      return rect;
   }
};

int main() {
   ::Image img = ::Image(3435);
   img.readImage();
   img.generateMask(3200);
   Index* index = img.maxIndex();
   std::cout << index->x << std::endl;
   std::cout << index->y << std::endl;
   //img.printData();
}
