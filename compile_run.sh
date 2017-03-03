echo "Compiling code..."
time g++ -W main.cpp -o main.o -lCCfits -lcfitsio -lm
echo "Compilation complete, running file..."
time ./main.o
