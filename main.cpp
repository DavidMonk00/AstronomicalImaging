#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <CCfits/CCfits>
#include <cmath>
#include <stdio.h>
#include <pthread.h>
#include "structs.h"

#define NUM_THREADS 4

using namespace std;

struct Helper;
vector<Index*> sources;

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
   valarray<unsigned long> contents;
   bool** mask;
   unsigned int cutoff;
   long ax0,ax1;
public:
   void init(int co) {
      cutoff = co;
   }
   void readImage() {
      auto_ptr<CCfits::FITS> pInfile(new CCfits::FITS("./A1_mosaic_mask.fits",CCfits::Read,true));
      CCfits::PHDU& image = pInfile->pHDU();
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
         ostream_iterator<short> c(cout, "\t");
         copy(&contents[j*ax0], &contents[(j+1)*ax0-1], c);
         cout << '\n';
      }
      cout << endl;
   }
   ThreadArgs generateArgs() {
      ThreadArgs td;
      td.ax0 = ax0;
      td.ax1 = ax1;
      td.mask = mask;
      td.data = data;
      td.cutoff = cutoff;
      return td;
   }
};

Index* maxIndex(ThreadArgs* args) {
   int i,j;
   Index* index = new Index;
   int rows = args->ax0/NUM_THREADS;
   int start = args->thread_id*rows;
   int end = (args->thread_id+1)*rows;
   unsigned int max = 0;
   for (i = start; i < end; i++) {
      for(j = 0; j < args->ax1; j++) {
         if (args->mask[i][j]) {
            if (args->data[i][j] > max) {
               max = args->data[i][j];
               index->x = i;
               index->y = j;
               index->max = max;
            }
         }
      }
   }
   cout << index->x << " " << index->y << " " << max << endl;
   return index;
}

void* thrd_findSources(void* threadargs) {
   ThreadArgs* args = (ThreadArgs*)threadargs;
   long ax0 = args->ax0;
   long ax1 = args->ax1;
   int a = args->aperture/2;
   int n = 0;
   while(true) {
      Index* centre = maxIndex(args);
      int x = centre->x;
      int y = centre->y;
      if (centre->max < args->cutoff) {
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
            args->mask[i][j] = false;
         }
      }
      delete centre;
   }
   pthread_exit(NULL);
}

void findSources(int aperture, ::Image* img) {
   ThreadArgs td[NUM_THREADS];

   pthread_t threads[NUM_THREADS];;
   pthread_attr_t attr;
   pthread_attr_init(&attr);
   pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);
   int i;
   for (i = 0; i < NUM_THREADS; i++) {
      td[i] = img->generateArgs();
      td[i].aperture = aperture;
      td[i].thread_id = i;
   }
   for (i = 0; i < NUM_THREADS; i++) {
      pthread_create(&threads[i], &attr, thrd_findSources, (void*)&td[i]);
      //thrd_findSources((void*)&td[i]);
   }
   void* status;
   for (i = 0; i < NUM_THREADS; i++) {
      pthread_join(threads[i],&status);
   }
}

int main() {
   ::Image img;
   img.init(3700);
   img.readImage();
   img.generateMask();
   findSources(12, &img);
}
