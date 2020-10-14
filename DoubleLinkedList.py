from DNode import Node
from typing import Optional, Tuple
from collections.abc import Iterable


class DLinkedList:
    def __init__(self, data=None, *, iterable=True, return_nodes=False):
        """
        :param data: data to add to linked list (if it is an iterable it will loop through and add each
        piece of data unless you specify iterable = False, then it will just add the iterable to one node)
        :param iterable: only set this to False if initializing with an iterable and you want that iterable
        to be stored in one node and not multiple nodes
        :param return_nodes: set this to True if you want return a list of Nodes instead of the data of each node
        """
        self.head = self.last = self.current = None
        self.return_nodes = return_nodes
        self.len = 0
        
        if data:
            if iterable:
                self.extend(data)
            else:
                self.add(data)

    def add(self, obj) -> None:
        """Append object to the end of the list."""
        last = Node(obj, prev=self.last)
        if self.head is None:
            self.current = self.head = last
        if self.last is not None:
            self.last.next = last
        self.last, self.len = last, self.len + 1

    def append(self, obj) -> None:
        """Append object to the end of the list."""
        self.add(obj)

    def index(self, obj, start: int = 0, stop: int = None) -> Optional[int]:
        """Return first index of value.
        Return None if the value is not present."""
        if stop is None:
            stop = self.len
        start, stop = (start if start >= 0 else self.len + start,
                       stop if stop >= 0 else self.len + stop)
        
        if start > stop or start > self.len - 1 or stop < 1:
            return None
        
        index, item = 0, self.head
        while item is not None:
            if item.data == obj and start <= index < stop:
                return index
            index, item = index + 1, item.next
        return None

    def get(self, index: int) -> Node:
        """Return Node of index (Node.data to get the value).
        Raises IndexError if index was out of range."""
        counter, item = 0, self.head
        index = index if index >= 0 else self.len + index

        if index == self.len - 1:
            return self.last

        if index < 0 or index > self.len - 1:
            raise IndexError("Index out of range")

        while True:
            if index == counter:  # 69 ... noice
                return item
            item = item.next
            counter += 1

    def insert(self, index: int, obj) -> None:
        """Insert object before index."""
        index = index if index >= 0 else self.len + index
        if index >= self.len:
            self.add(obj)

        elif index <= 0:
            self.current = self.head = Node(obj, self.head)
        else:
            old = self.get(index)
            old.prev.next = Node(obj, old, old.prev)

        self.len += 1

    def count(self, obj) -> int:
        """Return number of occurrences of value."""
        counter = 0
        item = self.head
        while item is not None:
            if item.data == obj:
                counter += 1
            item = item.next
        return counter

    def clear(self):
        """Remove all items."""
        self.head, self.len = None, 0

    def copy(self):
        """Return a copy of the DLL."""
        new = DLinkedList(return_nodes=self.return_nodes)
        item = self.head
        while item is not None:
            new.add(item)
            item = item.next
        return new

    def pop(self, index=...) -> None:
        """Remove and return item at index (default last).
        Raises IndexError if list is empty or index is out of range."""
        if self.head is None:
            raise IndexError("pop from empty DLinkedList")

        if index is ... or index == self.len - 1 or index == -1:
            item = self.last
            if self.last.prev is not None:
                self.last.prev.next = None
            else:
                self.head = None
            self.last = self.last.prev
        elif index == 0 or index == -self.len:
            item = self.head
            self.head = self.current = self.head.next
        else:
            item = obj = self.get(index)
            obj.prev.next = obj.next
        self.len -= 1
        return item.data

    def reverse(self) -> None:
        """Reverse in place."""
        item, new = self.head, DLinkedList(return_nodes=self.return_nodes)

        while item is not None:
            new.insert(0, item)
            item = item.next
        self.clear()
        self.extend(new)

    def sort(self, *, key=..., reverse: bool = False) -> None:
        """Stable sort in place."""
        if key is ...:
            new = DLinkedList(sorted(self.copy(), reverse=reverse), return_nodes=self.return_nodes)
        else:
            new = DLinkedList(sorted(self.copy(), key=key, reverse=reverse), return_nodes=self.return_nodes)
        self.clear()
        self.extend(new)

    def remove(self, obj) -> None:
        """Remove first occurrence of value.
        Remove nothing if the value is not present."""
        item = self.head
        if self.head.data == obj:
            self.head = self.head.next
            self.current = self.head
        else:
            while item is not None:
                if item.data == obj:
                    item.prev.next = item.next
                    if item.next is None:
                        self.last = self.last.prev
                    break
                item = item.next
            else:
                return
        self.len -= 1

    def extend(self, obj):
        """Extend list by appending elements from the iterable."""
        if isinstance(obj, DLinkedList):
            obj = obj.copy()
            if self.len > 0:
                self.last.next = obj.head
                self.last.next.prev = self.last
            else:
                self.head = obj.head
                self.current = self.head
            self.last = obj.last
            self.len += obj.__len__()
        else:
            for x in obj:
                self.add(x)

    def __len__(self) -> int:
        """Return len(self)."""
        return self.len

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"""DLL({', '.join('DLL(...)' if isinstance(x, DLinkedList) and self in x
                                  else f'{x!r}' for x in self)})"""

    def __iter__(self):
        """Implement iter(self)."""
        item = self.head
        if self.return_nodes:
            while item is not None:
                yield item
                item = item.next
        else:
            while item is not None:
                yield item.data
                item = item.next

    def __add__(self, other):
        """Return self+other."""
        old = DLinkedList(self.copy(), return_nodes=self.return_nodes)
        self.extend(other)
        new = self.copy()
        self.clear()
        self.extend(old)
        return new

    def __radd__(self, other):
        """return other+self."""
        old = DLinkedList(self.copy(), return_nodes=self.return_nodes)
        self.clear()
        self.extend(other)
        self.extend(old)
        new = self.copy()
        self.clear()
        self.extend(old)
        return new

    def __mul__(self, other: int):
        """return self*other."""
        new = DLinkedList(return_nodes=self.return_nodes)
        for _ in range(abs(other)):
            new.extend(self.copy())
        if other < 0:
            new.reverse()
        return new

    def __rmul__(self, other: int):
        """Return other*self."""
        return self.__mul__(other)

    def __reversed__(self):
        """return reversed(self)."""
        new = DLinkedList(self.copy(), return_nodes=self.return_nodes)
        new.reverse()
        return new

    def __item__(self, item: slice) -> Tuple[int, int, int]:
        step = item.step or 1
        start, stop = (item.start or (0 if step > 0 else self.len - 1),
                       item.stop or (self.len if step > 0 else -1))

        if not all(isinstance(x, int) for x in (start, stop, step)):
            raise TypeError("only 'int' type is acceptable")

        if item.step == 0:
            raise ValueError("slice step cannot be zero")

        start, stop = (start if start > -1 else self.len + start,
                       stop if stop > (-1 if step > 0 else -2) else self.len + stop)

        if (step > 0 and (start >= self.len or stop <= 0 or start >= stop))\
                or (step < 0 and (start <= 0 or stop >= self.len or start <= stop)):
            return 0, 0, step

        start, stop = (max(start, 0), min(stop, self.len)) if step > 0 else (min(start, self.len - 1), max(stop, -1))

        return start, stop, step

    def __getitem__(self, item):
        """x.__getitem__(y) <==> x[y]."""
        if isinstance(item, int):
            r = self.get(item)
            if self.return_nodes:
                return r
            return r.data

        elif isinstance(item, slice):
            start, stop, step = self.__item__(item)
            new, counter = DLinkedList(return_nodes=self.return_nodes), start
            print(start, stop, step)
            while counter < stop if step > 0 else counter > stop:
                new.add(self.get(counter).data)
                counter += step
            return new
        else:
            raise TypeError('Invalid index type given (accepted indexes: int, slice)')

    def __delitem__(self, item) -> None:
        """Delete self[key]."""
        if isinstance(item, int):
            self.pop(item)

        elif isinstance(item, slice):
            start, stop, step = self.__item__(item)
            indexes, new = range(start, stop, step), DLinkedList(return_nodes=self.return_nodes)

            for i, x in enumerate(self):
                if i not in indexes:
                    new.add(x)
            self.clear()
            self.extend(new)
        else:
            raise TypeError('Invalid index type given (accepted indexes: int, slice)')

    def __setitem__(self, item, value):
        """Set self[key] to value."""
        if isinstance(item, int):
            self.get(item).data = value

        elif isinstance(item, slice):
            if not isinstance(value, Iterable):
                raise TypeError("can only assign an iterable")

            start, stop, step = self.__item__(item)
            if step != 1:
                s = (stop - start + (step > 0 or - 1))
                # noinspection PyTypeChecker
                if s // step != len(value):
                    # noinspection PyTypeChecker
                    raise ValueError(f"attempt to assign sequence of size {len(value)}"
                                     f" to extended slice of size {s // step}")
                v = iter(value)
                for x, y in zip(range(start, stop, step), value):
                    self.get(x).data = next(v)
            else:
                new = DLinkedList(value, return_nodes=self.return_nodes)
                new.reverse()
                del self[start:stop:step]

                for x in new:
                    self.insert(start, x)
        else:
            raise TypeError('Invalid index type given (accepted indexes: int, slice)')

    def __gt__(self, other) -> bool:
        """return self > other."""
        if not isinstance(other, (list, DLinkedList)):
            raise TypeError(f"""'>' not supported between instances
                                of 'DLinkedList' and'{str(type(other)).split("'")[1]}'""")
        for x, y in zip(self, other):
            if x > y:
                return True
            if x < y:
                return False
        return self.len > len(other)

    def __ge__(self, other) -> bool:
        """Return self >= other."""
        if not isinstance(other, (list, DLinkedList)):
            raise TypeError(f"""'>=' not supported between instances
                                of 'DLinkedList' and'{str(type(other)).split("'")[1]}'""")
        for x, y in zip(self, other):
            if x < y:
                return False
        return self.len >= len(other)

    def __lt__(self, other) -> bool:
        """Return self < other."""
        if not isinstance(other, (list, DLinkedList)):
            raise TypeError(f"""'<' not supported between instances
                                of 'DLinkedList' and'{str(type(other)).split("'")[1]}'""")
        for x, y in zip(self, other):
            if x < y:
                return True
            if x > y:
                return False
        return self.len < len(other)

    def __le__(self, other) -> bool:
        """Return self <= other."""
        if not isinstance(other, (list, DLinkedList)):
            raise TypeError(f"""'<=' not supported between instances
                                of 'DLinkedList' and'{str(type(other)).split("'")[1]}'""")
        for x, y in zip(self, other):
            if x > y:
                return False
        return self.len <= len(other)

    def __eq__(self, other) -> bool:
        """Return self == other."""
        # noinspection PyTypeChecker
        if isinstance(other, Iterable) and self.len == len(other):
            if other in self and self in other:
                return True
            for x, y in zip(self, other):
                if x != y:
                    return False
            return True
        return False

    def __bool__(self) -> bool:  # 420 ... nice
        """Return bool(self), False if it was empty otherwise True."""
        return self.head is not None

    def __ne__(self, other) -> bool:
        """Return self != other"""
        return not self.__eq__(other)

    def __neg__(self):
        """Return -self, reverse the DLL in place"""
        return self.__reversed__()

    def __next__(self):
        """Implement next(self)."""
        if self.current is None or self.head is None:
            raise StopIteration
        current, self.current = self.current, self.current.next
        return current.data

    def __truediv__(self, other: int):
        """Return self / other, splits the DLL items into group of DLLs"""
        if not isinstance(other, int):
            raise TypeError(f"""'/' not supported between instances
                                            of 'DLinkedList' and'{str(type(other)).split("'")[1]}'""")
        new, copy, i = DLinkedList(return_nodes=self.return_nodes), self.copy(), round((self.len+.1)/other) or 1
        counter = 0
        for x in range(min(other, self.len)):
            new.add(copy[counter:counter+i])
            counter += i
        return new  # 420 ... perfect
