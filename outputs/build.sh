set -e
export PATH=/ucrt64/bin:/usr/bin:$PATH
cd "/d/_Personal/Random Projects/TREE-QMC/outputs/tqmc_pre_network"
g++ --version | head -1; make --version | head -1
(cd external/MQLib && make CFLAGS="-Iinclude -std=c++0x -O2 -Wall -D_USE_MATH_DEFINES")
mkdir -p build && cd build
g++ -std=c++11 -O2 -I ../external/MQLib/include -I ../external/toms743 -o tree-qmc \
  ../src/*.cpp ../external/toms743/toms743.cpp ../external/MQLib/bin/MQLib.a -lm -DVERSION=\"$(cat ../version.txt)\"
ls -la tree-qmc*
