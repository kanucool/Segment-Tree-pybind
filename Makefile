PYTHON_INCLUDES := $(shell python3.13-config --includes)
PYTHON_LDFLAGS := $(shell python3.13-config --ldflags)

# Replace with your own path
PYBIND11_INCLUDE_PATH = /home/kanucool/.local/lib/python3.13/site-packages/pybind11/include

# Compiler
CXX = g++

# Flags
CXXFLAGS = -Wall -Werror $(PYTHON_INCLUDES) -I$(PYBIND11_INCLUDE_PATH)
LD_FLAGS = $(PYTHON_LDFLAGS)

# Target and sources
TARGET = segment_tree_cpp.so
SRC = SegmentTree.cpp
OBJ = $(SRC:.cpp=.o)

# Create the executable
$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) -shared -O3 -fPIC -o $@ $^ $(LD_FLAGS)

# Create the object files
%.o: %.cpp SegmentTree.hpp
	$(CXX) $(CXXFLAGS) -O3 -fPIC -c $< -o $@

clean:
	rm -f $(TARGET) *.o

