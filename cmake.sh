cmake -GNinja -B ../cg-build/ -S .     -DCMAKE_BUILD_TYPE=RelWithDebInfo     -DIREE_ENABLE_ASSERTIONS=ON     -DCMAKE_C_COMPILER=clang     -DCMAKE_CXX_COMPILER=clang++     -DIREE_ENABLE_LLD=ON
