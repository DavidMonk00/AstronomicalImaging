rm ./C++/main.o
echo "Compiling code..."
g++ -W ./C++/main.cpp -o ./C++/main.o -lCCfits -lcfitsio -lm -lpthread
echo "Compilation complete, running file..."
echo "Generating masked image..."
python ./python/mask.py
echo "Finding sources..."
#for i in {3500..4000..100}
#do
#   echo $i
#   ./main.o $i $1
#done
./C++/main.o 3600 $1
echo "Plotting..."
python ./python/photometry.py $1
