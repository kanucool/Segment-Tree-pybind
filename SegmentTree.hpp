#pragma once
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <limits>
#include <functional>
#include <cstddef>
#include <typeinfo>

namespace py = pybind11;

template <typename T>
class __attribute__((visibility("default"))) SegmentTree {
private:
    size_t N;
    T defValue;
    std::vector<T> tree;
    py::function combinePy;
    T (*combineCpp)(const T&, const T&) = nullptr;
    bool isCppNative = false;

    void build() {
        for (size_t i = N - 1; i > 0; i--) {
            tree[i] = combine(tree[i << 1], tree[i << 1 | 1]);
        }
    }

    T combine(const T& a, const T& b) {
        if (isCppNative) return combineCpp(a, b);
        else return combinePy(a, b).template cast<T>();
    }

public:
    SegmentTree(const std::vector<T> &arr, py::function &combine, T defValue)
        : N(arr.size()), defValue(defValue), tree(N << 1, defValue), combinePy(combine), isCppNative(false)
    {
        for (size_t i = 0; i < N; i++) {
            tree[N + i] = arr[i];
        }
        build();
    }

    SegmentTree(const std::vector<T> &arr, T (*combine)(const T&, const T&), T defValue)
        : N(arr.size()), defValue(defValue), tree(N << 1, defValue), combineCpp(combine), isCppNative(true)
    {
        for (size_t i = 0; i < N; i++) {
            tree[N + i] = arr[i];
        }
        build();
    }

    void update(size_t idx, const T &val) {
        idx += N;
        tree[idx] = val;
        idx >>= 1;
        while (idx > 0) {
            tree[idx] = combine(tree[idx << 1], tree[idx << 1 | 1]);
            idx >>= 1;
        }
    }

    T query(size_t l, size_t r) {
        T resL = defValue;
        T resR = defValue;
        l += N;
        r += N;
        while (l < r) {
            if (l & 1) resL = combine(resL, tree[l++]);
            if (r & 1) resR = combine(tree[--r], resR);
            l >>= 1;
            r >>= 1;
        }
        return combine(resL, resR);
    }
};
