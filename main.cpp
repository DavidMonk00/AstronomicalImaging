#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <CCfits/CCfits>
#include <cmath>

using namespace CCfits;

class Image {
private:
   unsigned long** data;
   std::valarray<unsigned long> contents;
   bool** mask;
   long ax0,ax1;
public:
   void readImage() {
      std::auto_ptr<FITS> pInfile(new FITS("./A1_mosaic.fits",Read,true));
      PHDU& image = pInfile->pHDU();
      image.readAllKeys();
      image.read(contents);
      //std::cout << image << std::endl;
      std::cout << image.axis(0) << std::endl;
      std::cout << image.axis(1) << std::endl;
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
};


int main() {
   ::Image img;
   img.readImage();
   img.generateMask(3200);
   //img.printData();
}
