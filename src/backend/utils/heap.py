class Heap:
    def __init__(self, comparator=None, max_size=float('inf')):
        # Default comparator for min-heap
        self.heap = []
        self.comparator = comparator if comparator is not None else lambda a, b: a - b
        self.max_size = max_size

    # --- UTILITY METHODS --- #

    def peek(self):
        return self.heap[0] if self.size() > 0 else None

    def size(self):
        return len(self.heap)

    def is_empty(self):
        return self.size() == 0

    def is_full(self):
        return self.size() == self.max_size

    def has_items(self):
        return self.size() > 0

    def get_left_index(self, index):
        return 2 * index + 1

    def get_right_index(self, index):
        return 2 * index + 2

    def get_parent_index(self, index):
        return (index - 1) // 2

    def swap(self, a, b):
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    def extract(self):
        array = []
        while self.has_items():
            array.append(self.pop())
        return array

    def to_array(self):
        # Make a copy of the heap and return it as a list
        copy = Heap(comparator=self.comparator, max_size=self.max_size)
        copy.heap = self.heap[:]
        return copy.extract()

    # --- ITEM INSERTION --- #

    def push(self, data):
        if data is None:
            return False

        self.heap.append(data)
        self.bubble_up(self.size() - 1)

        if self.size() > self.max_size:
            self.pop()

        return True

    def bubble_up(self, index):
        while index > 0:
            curr = self.heap[index]
            parent_index = self.get_parent_index(index)
            parent = self.heap[parent_index]

            if self.comparator(parent, curr) <= 0:
                break

            self.swap(index, parent_index)
            index = parent_index

    # --- ITEM DELETION --- #

    def pop(self):
        if self.size() == 0:
            return None

        if self.size() == 1:
            return self.heap.pop(0)

        value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.bubble_down(0)
        return value

    def bubble_down(self, curr_index):
        left = self.get_left_index(curr_index)
        right = self.get_right_index(curr_index)
        parent_index = curr_index

        if left < self.size() and self.comparator(self.heap[left], self.heap[parent_index]) < 0:
            parent_index = left

        if right < self.size() and self.comparator(self.heap[right], self.heap[parent_index]) < 0:
            parent_index = right

        if parent_index != curr_index:
            self.swap(parent_index, curr_index)
            self.bubble_down(parent_index)
