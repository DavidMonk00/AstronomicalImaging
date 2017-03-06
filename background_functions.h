
int maxIndex(unsigned int** data, long ax0, long ax1) {
	int i,j;
	int max = 0;
	for (i = 0; i < ax0; i++) {
		for(j = 0; j < ax1; j++) {
			if (data[i][j] > max) {
				max = data[i][j]
			}
		}
	}
	return max;
}
