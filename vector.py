
import ctypes
from typing import Iterable, Optional, TypeVar, Iterator

T = TypeVar('T')

class Vector:
    def __init__(self, iterable: Optional[Iterable[T]] = None):
        self._n = 0            
        self._capacity = 1     
        self._A = self._make_array(self._capacity)
        if iterable:
            for item in iterable:
                self.append(item)

    def __len__(self) -> int:
        return self._n

    def __bool__(self) -> bool:
        return self._n != 0

    def __getitem__(self, k: int) -> T:
        if not 0 <= k < self._n:
            raise IndexError('Index out of bounds')
        return self._A[k]

    def __setitem__(self, k: int, value: T) -> None:
        if not 0 <= k < self._n:
            raise IndexError('Index out of bounds')
        self._A[k] = value

    def __repr__(self) -> str:
        return f"Vector([{', '.join(str(self._A[i]) for i in range(self._n))}])"

    def __iter__(self) -> Iterator[T]:
        for i in range(self._n):
            yield self._A[i]

    def __contains__(self, item: T) -> bool:
        for i in range(self._n):
            if self._A[i] == item:
                return True
        return False

    def append(self, obj: T) -> None:
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        self._A[self._n] = obj
        self._n += 1

    def insert(self, k: int, value: T) -> None:
        if not 0 <= k <= self._n:
            raise IndexError('Index out of bounds')
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        for j in range(self._n, k, -1):
            self._A[j] = self._A[j-1]
        self._A[k] = value
        self._n += 1

    def remove(self, value: T) -> None:
        for k in range(self._n):
            if self._A[k] == value:
                for j in range(k, self._n-1):
                    self._A[j] = self._A[j+1]
                self._A[self._n-1] = None
                self._n -= 1
                return
        raise ValueError("Value not found")

    def pop(self) -> T:
        if self._n == 0:
            raise IndexError("Pop from empty vector")
        val = self._A[self._n-1]
        self._A[self._n-1] = None
        self._n -= 1
        return val

    def _resize(self, c: int) -> None:
        B = self._make_array(c)
        for k in range(self._n):
            B[k] = self._A[k]
        self._A = B
        self._capacity = c

    def _make_array(self, c: int):
        return (c * ctypes.py_object)()

    def copy(self) -> 'Vector[T]':
        v = Vector()
        for i in range(self._n):
            v.append(self._A[i])
        return v

    def to_list(self) -> list:
        return [self._A[i] for i in range(self._n)]

    def index(self, value: T) -> int:
        for i in range(self._n):
            if self._A[i] == value:
                return i
        raise ValueError('Value not found')

    def extend(self, iterable: Iterable[T]) -> None:
        for item in iterable:
            self.append(item)
