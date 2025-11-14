## Faster Segment Tree in Python using C++ and PyBind

Uses PyBind to make a C++ segment tree usable in Python.
SegmentTree.min(), SegmentTree.max(), SegmentTree.sum() use native C++ and offer significant speed boosts over a native Python implementation.
You can also pass in Python objects / a Python merge function to SegmentTree(), which offers no speed advantage but provides flexibility.

To generate the shared object file (segment_tree_cpp.so), just run ``make``.
To import into Python, put ``from segment_tree_cpp import SegmentTree`` at the top of your file.
