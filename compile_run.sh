
rm ./main.o
echo "Compiling code..."
time g++ -W main.cpp -o main.o -lCCfits -lcfitsio -lm
echo "Compilation complete, running file..."
echo "Generating masked image..."
python mask.py
echo "Finding sources..."
time ./main.o
