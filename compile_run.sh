rm ./C++/main.o
echo "Compiling code..."
g++ ./C++/main.cpp -o ./C++/main.o -lCCfits -lcfitsio -lm -lpthread
echo "Compilation complete, running file..."
echo "Generating masked image..."
python ./python/mask.py
echo "Finding sources..."
#for i in {3500..4000..100}
#do
#   echo $i
#   ./main.o $i $1
#done
./C++/main.o $2 $1
echo "Source detection complete. Starting photometry..."
python -W ignore ./python/photometry.py $1 $2

