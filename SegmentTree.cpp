#include "SegmentTree.hpp"

using lint = long long;

auto minDouble = [](const double &a, const double &b) {return std::min(a, b);};
auto maxDouble = [](const double &a, const double &b) {return std::max(a, b);};
auto sumDouble = [](const double &a, const double &b) {return a + b;};

auto minLint = [](const lint &a, const lint &b) {return std::min(a, b);};
auto maxLint = [](const lint &a, const lint &b) {return std::max(a, b);};
auto sumLint = [](const lint &a, const lint &b) {return a + b;};


template <typename T>
void registerTreeType(py::module_ &m) {
    py::class_<SegmentTree<T>>(m, typeid(T).name())
    .def("update", &SegmentTree<T>::update)
    .def("query", &SegmentTree<T>::query);
}

template <typename T, typename Combine>
py::object getSpecializedTree(py::list &arr, Combine combine, py::object &defValue, T fallbackDefault) {
    auto vec = arr.cast<std::vector<T>>();
    T defVal = defValue.is_none() ? fallbackDefault: defValue.cast<T>();
    return py::cast(SegmentTree<T>(vec, combine, defVal));
}

PYBIND11_MODULE(segment_tree_cpp, m) {
    registerTreeType<lint>(m);
    registerTreeType<double>(m);

    py::class_<SegmentTree<py::object>>(m, "SegmentTree")
    .def(
        py::init<
            const std::vector<py::object> &,
            py::function &,
            py::object
        >(),
        py::arg("arr"),
        py::arg("combine"),
        py::arg("defValue")
    )
    .def_static("min", 
        [](py::list arr, py::object defValue = py::none()) -> py::object {
            if (arr.empty()) throw std::runtime_error("Array must be non-empty");
            py::object num = arr[0];

            if (py::isinstance<py::float_>(num)) {
                return getSpecializedTree<double>(arr, minDouble, defValue, std::numeric_limits<double>::max());
            }   
            else if (py::isinstance<py::int_>(num)) {
                return getSpecializedTree<lint>(arr, minLint, defValue, std::numeric_limits<lint>::max());
            }
            throw std::runtime_error("Incompatible type: must be numerical");
        },
        py::arg("arr"),
        py::arg("defValue") = py::none()
    )
    .def_static("max", 
        [](py::list arr, py::object defValue = py::none()) -> py::object {
            if (arr.empty()) throw std::runtime_error("Array must be non-empty");
            py::object num = arr[0];

            if (py::isinstance<py::float_>(num)) {
                return getSpecializedTree<double>(arr, maxDouble, defValue, std::numeric_limits<double>::lowest());
            }   
            else if (py::isinstance<py::int_>(num)) {
                return getSpecializedTree<lint>(arr, maxLint, defValue, std::numeric_limits<lint>::lowest());
            }
            throw std::runtime_error("Incompatible type: must be numerical");
        },
        py::arg("arr"),
        py::arg("defValue") = py::none()
    )
    .def_static("sum", 
        [](py::list arr, py::object defValue = py::none()) -> py::object {
            if (arr.empty()) throw std::runtime_error("Array must be non-empty");
            py::object num = arr[0];

            if (py::isinstance<py::float_>(num)) {
                return getSpecializedTree<double>(arr, sumDouble, defValue, 0.0);
            }   
            else if (py::isinstance<py::int_>(num)) {
                return getSpecializedTree<lint>(arr, sumLint, defValue, 0);
            }
            throw std::runtime_error("Incompatible type: must be numerical");
        },
        py::arg("arr"),
        py::arg("defValue") = py::none()
    )
    .def(
        "update", &SegmentTree<py::object>::update
    )
    .def(
        "query", &SegmentTree<py::object>::query
    );
}
