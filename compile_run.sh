rm ./main.o
echo "Compiling code..."
time g++ -W main.cpp -o main.o -lCCfits -lcfitsio -lm -lpthread
echo "Compilation complete, running file..."
echo "Generating masked image..."
python mask.py
echo "Finding sources..."
for i in {3500..4000..100}
do
   echo $i
   ./main.o $i $1
done
echo "Plotting..."
python plotsources.py $1
