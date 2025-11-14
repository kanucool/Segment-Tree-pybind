class SegmentTree:
    def __init__(self, arr, combine, defValue):
        self.N = len(arr)
        self.defValue = defValue
        self.combine = combine
        self.tree = [defValue] * (self.N * 2)

        for i in range(self.N):
            self.tree[self.N + i] = arr[i]

        for i in range(self.N - 1, 0, -1):
            self.tree[i] = self.combine(self.tree[i << 1], self.tree[i << 1 | 1])

    def update(self, idx, val):
        idx += self.N
        self.tree[idx] = val
        idx >>= 1
        while idx > 0:
            self.tree[idx] = self.combine(self.tree[idx << 1], self.tree[idx << 1 | 1])
            idx >>= 1

    def query(self, l, r):
        resL = self.defValue
        resR = self.defValue
        l += self.N
        r += self.N
        while l < r:
            if l & 1:
                resL = self.combine(resL, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                resR = self.combine(self.tree[r], resR)
            l >>= 1
            r >>= 1
        return self.combine(resL, resR)
    
def main():
    print("TEST")

if __name__ == "__main__":
    main()
