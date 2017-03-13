rm ./main.o
echo "Compiling code..."
g++ -W main.cpp -o main.o -lCCfits -lcfitsio -lm -lpthread
echo "Compilation complete, running file..."
echo "Generating masked image..."
python mask.py
echo "Finding sources..."
#for i in {3500..4000..100}
#do
#   echo $i
#   ./main.o $i $1
#done
./main.o 3600 $1
echo "Plotting..."
python photometry.py $1
