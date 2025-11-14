from __future__ import annotations
import random
import time
from statistics import mean
from typing import Union, Callable, Any
from enum import Enum

from segment_tree_cpp import SegmentTree as CppSegtree
from PythonSegtree import SegmentTree as PythonSegtree

class SpecializationEnum(Enum):
    NONE = -1
    SUM = 0
    MIN = 1
    MAX = 2

class PyObject:
    def __init__(self,):
        self.val = random.uniform(0.0, 10 ** 5)
        self.valInt = random.randint(0, 10 ** 5)
        self.string = f"{self.val}--{self.valInt}"
    
    def __eq__(self, other: PyObject) -> bool:
        return (
            self.val == other.val and
            self.valInt == other.valInt and
            self.string == other.string
        )

def runQueries(segTree: Union[CppSegtree, PythonSegtree], ops: list[tuple],) -> list:
    values = []
    for qType, query in ops:
        if qType == "update":
            segTree.update(*query)
        else:
            values.append(segTree.query(*query))
    return values

def generateOps(N: int, queryRatio: float, randomValue: Callable,):
    numQueries = int(N * queryRatio)
    numUpdates = N - numQueries

    updates = [(random.randint(0, N - 1), randomValue()) for _ in range(numUpdates)]
    queries = [random.randint(0, N - 1) for _ in range(numQueries)]
    queries = [(qStart, random.randint(qStart + 1, N)) for qStart in queries]

    allOps = []
    uPtr = qPtr = 0
    while uPtr < numUpdates or qPtr < numQueries:
        choices = []
        if uPtr < numUpdates: choices.append("update")
        if qPtr < numQueries: choices.append("query")
        choice = random.choice(choices)

        if choice == "update":
            allOps.append(("update", updates[uPtr]))
            uPtr += 1
        else:
            allOps.append(("query", queries[qPtr]))
            qPtr += 1

    return allOps

def benchmark(
                arr: list,
                randomValue: Callable,
                combine: Callable,
                defValue: Any,
                queryRatio: float = 0.5,
                specialization: SpecializationEnum = SpecializationEnum.NONE,
              ) -> dict:
    N = len(arr)
    assert N
    
    operations = generateOps(N, queryRatio, randomValue)
    
    # Benchmarking step
    times = {}

    cppStart = time.time()

    if specialization == SpecializationEnum.NONE:
        cppSeg = CppSegtree(arr=arr, combine=combine, defValue=defValue,)
    elif specialization == SpecializationEnum.MIN:
        cppSeg = CppSegtree.min(arr=arr,)
    elif specialization == SpecializationEnum.MAX:
        cppSeg = CppSegtree.max(arr=arr,)
    else:
        cppSeg = CppSegtree.sum(arr=arr,)

    cppVals = runQueries(segTree=cppSeg, ops=operations)

    cppEnd = time.time()
    times["cpp"] = cppEnd - cppStart

    pyStart = time.time()

    pySeg = PythonSegtree(arr=arr, combine=combine, defValue=defValue)
    pyVals = runQueries(segTree=pySeg, ops=operations)

    pyEnd = time.time()
    times["py"] = pyEnd - pyStart

    assert cppVals == pyVals
    return times

def testFloatSum(N: int) -> dict:
    arr = []
    def randomValue(): return random.uniform(-10 ** 6, 10 ** 6)
    for _ in range(N): arr.append(randomValue())
    return benchmark(arr=arr, randomValue=randomValue,
                     combine=lambda a, b: a + b, defValue=0, specialization=SpecializationEnum.SUM,)

def testLintSum(N: int) -> dict:
    arr = []
    def randomValue(): return random.randint(-10 ** 6, 10 ** 6)
    for _ in range(N): arr.append(randomValue())
    return benchmark(arr=arr, randomValue=randomValue,
                     combine=lambda a, b: a + b, defValue=0, specialization=SpecializationEnum.SUM,)

def testFloatMax(N: int) -> dict:
    arr = []
    def randomValue(): return random.uniform(-10 ** 6, 10 ** 6)
    for _ in range(N): arr.append(randomValue())
    return benchmark(arr=arr, randomValue=randomValue,
                     combine=max, defValue=-float('inf'), specialization=SpecializationEnum.MAX,)

def testLintMax(N: int) -> dict:
    arr = []
    def randomValue(): return random.randint(-10 ** 6, 10 ** 6)
    for _ in range(N): arr.append(randomValue())
    return benchmark(arr=arr, randomValue=randomValue,
                     combine=max, defValue=-10 ** 10, specialization=SpecializationEnum.MAX,)

def testPyObject(N: int) -> dict:
    arr = []
    def randomValue(): return PyObject()
    for _ in range(N): arr.append(randomValue())
    def combine(a: PyObject, b: PyObject) -> PyObject:
        newObj = PyObject()
        newObj.val = max(a.val, b.val)
        newObj.valInt = sum((a.valInt, b.valInt))
        newObj.string = a.string[::-1] + b.string[-1]
        return newObj
    return benchmark(arr=arr, randomValue=randomValue,
                     combine=combine, defValue=PyObject())

def main():
    times = testFloatSum(10 ** 6)
    print("Float sum")
    print(f"C++: {times['cpp']}\nPython: {times['py']}")

    times = testLintSum(10 ** 6)
    print("\nLint sum")
    print(f"C++: {times['cpp']}\nPython: {times['py']}")

    times = testFloatMax(10 ** 6)
    print("\nFloat max")
    print(f"C++: {times['cpp']}\nPython: {times['py']}")

    times = testLintMax(10 ** 6)
    print("\nLint max")
    print(f"C++: {times['cpp']}\nPython: {times['py']}")

    times = testPyObject(10 ** 6)
    print("\nPyObject")
    print(f"C++: {times['cpp']}\nPython: {times['py']}")

if __name__ == "__main__": main()
