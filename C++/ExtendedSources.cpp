#include <fstream>
#include <iostream>
#include <stdio.h>
#include <string>
#include <vector>

using namespace std;

struct Source {
	int x;
	int y;
	int flux;
	int a;
	int b;
};

int main(void) {
	ifstream file;
	file.open("../data/sources_10_3450.csv");
	string value;
	int n;
	vector<Source> srcs;
	while(file.good()) {
		n++;
		Source src;
		getline(file,value,',');
		src.x = stoi(value);
		getline(file,value,',');
		src.y = stoi(value);
		getline(file,value,',');
		src.flux = stoi(value);
		//cout << stoi(value) << endl;
		srcs.push_back(src);
	}
	cout << n << endl;
}
