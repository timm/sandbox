def binarysearch(sequence, value):
    lo, hi = 0, len(sequence) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sequence[mid] < value:
            lo = mid + 1
        elif value < sequence[mid]:
            hi = mid - 1
        else:
            return mid
    return mid

print(binarysearch([1,2,3,4],2))
print(binarysearch([1,2,3,4],0.11))
print(binarysearch([1,2,3,4],2))


