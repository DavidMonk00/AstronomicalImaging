struct Index {
   int x;
   int y;
   unsigned int max;
};

struct ThreadArgs {
   int aperture;
   long ax0;
   long ax1;
   int thread_id;
   bool** mask;
   unsigned long** data;
   unsigned int cutoff;
};
