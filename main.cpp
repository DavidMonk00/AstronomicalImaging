#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <CCfits/CCfits>
#include <cmath>

using namespace CCfits;

int readImage() {
   std::auto_ptr<FITS> pInfile(new FITS("./A1_mosaic.fits",Read,true));
   PHDU& image = pInfile->pHDU();
   std::valarray<unsigned long> contents;
   image.readAllKeys();
   image.read(contents);
   std::cout << image << std::endl;
   long ax1(image.axis(0));
   long ax2(image.axis(1));

   /*for (long j = 0; j < ax2; j += 10) {
      std::ostream_iterator<short> c(std::cout, "\t");
      std::copy(&contents[j*ax1], &contents[(j+1)*ax1-1], c);
      std::cout << '\n';
   }*/
   std::cout << std::endl;
   return 0;
}

int main() {
   readImage();
}
