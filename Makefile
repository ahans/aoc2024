day17_2: Makefile day17_2.cu
	nvcc -O2 -o day17_2 -std=c++17 --expt-relaxed-constexpr day17_2.cu

clean:
	rm -rf day17_2
