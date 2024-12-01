from typing import Any


class Queue:
    """A simple class that creates a queue of values to be processed in order. Can be called to get the next value in
    the queue or to add a value to the queue if an argument is passed. Functionally identical to the Stack class but
    with a different order of processing.

    Methods:
        add(value: Any) -> None:
            Add a value to the back of the queue.
        pop(distance: int = 0) -> Any | None:
            Remove and return the next value in the queue.
        peek(distance: int = 0) -> Any | None:
            Return the next value in the queue without removing it.
    """

    def __init__(self, values: list[Any] | None = None) -> None:
        """Initialize the Queue object.

        Args:
            values (list[Any] | None, optional):
                The values to add to the queue.
                Defaults to [] if None.
        """
        if values is None:
            values = []
        self._queue = values

    @property
    def queue(self) -> list[Any]:
        return self._queue

    @queue.setter
    def queue(self, values: list[Any]) -> None:
        self._queue = values

    @queue.deleter
    def queue(self) -> None:
        self._queue.clear()

    def add(self, value: Any) -> None:
        """Add a value to the back of the queue.

        Args:
            value (Any):
                The value to add to the back of the queue.
        """
        self._queue.append(value)

    def insert(self, value: Any, distance: int = 0) -> None:
        """Insert a value into the queue at a specified distance from the front of the queue. (Or back if negative.)

        Args:
            value (Any):
                The value to insert into the queue.
            distance (int, optional):
                The distance from the front of the queue to insert the value.
                Defaults to 0.
        """
        self._queue.insert(distance, value)

    def pop(self, distance: int = 0) -> Any | None:
        """Remove and return the next value in the queue.

        Returns:
            Any: The next value in the queue.
            None: If the queue is empty.
        """
        # If the distance is out of bounds, return None. This also catches the case where the queue is empty.
        if distance >= len(self._queue) or abs(distance) > len(self._queue):
            return None

        return self._queue.pop(distance) if self._queue else None

    def peek(self, distance: int = 0) -> Any | None:
        """Return the next value in the queue without removing it.

        Args:
            distance (int, optional):
                The distance from the front of the queue to peek at.
                Defaults to 0.

        Returns:
            Any: The next value in the queue.
            None: If the queue is empty or the distance is out of bounds.
        """
        # If the distance is out of bounds, return None. This also catches the case where the queue is empty.
        if distance >= len(self._queue) or abs(distance) > len(self._queue):
            return None

        return self._queue[distance]

    def remove(self, value: Any, quantity: int = 1, reverse: bool = False) -> None:
        """Remove a value from the queue. Note that this will remove all instances of the value.

        Args:
            value (Any):
                The value to remove from the queue.
            quantity (int, optional):
                The number of instances of the value to remove. Set to -1 to remove all instances. Instances are
                removed in the order they appear in the queue from front to back.
                Defaults to 1.
            reverse (bool, optional):
                Whether to remove the instances of the value from back to front instead of front to back.
                Defaults to False.
        """
        if quantity == -1:
            self._queue = [item for item in self._queue if item != value]
            return

        for _ in range(quantity):
            index = self.index(value, reverse=reverse)

            if index is not None:
                del self._queue[index]
            else:
                return

    def remove_at(self, index: int) -> None:
        """Remove a value from the queue at a specified index.

        Args:
            index (int):
                The distance from the front of the queue to remove the value.
        """
        del self._queue[index]

    def index(self, value: Any, instance: int = 0, reverse: bool = False) -> int | None:
        """Return the first index of a value in the queue.

        Args:
            value (Any):
                The value to find the index of.
            instance (int, optional):
                The instance of the value to find the index of.
                Defaults to 0. (The first instance.)
            reverse (bool, optional):
                Whether to find the index of the value from back to front instead of front to back.
                Defaults to False.

        Returns:
            int: The index of the value. Indexing starts at the front of the queue unless reverse is True.
            None: If the value is not in the queue or the instance is out of bounds.
        """
        # Find all instances of the value in the queue.
        instances = [i for i, item in enumerate(self._queue) if item == value]

        # Reverse the list of instances if reverse is True.
        instances = instances[::-1] if reverse else instances

        # If the instance of the value is not in the queue, return None.
        if instance >= len(instances) or abs(instance) > len(instances):
            return None

        return instances[instance]

    def __repr__(self) -> str:
        return str(self._queue[0] if self._queue else None)

    def __bool__(self) -> bool:
        return bool(self._queue)

    def __call__(self, value: Any = None) -> Any:
        if value is not None:
            self._queue.append(value)
            return None

        return self._queue.pop(0) if self._queue else None

    def __len__(self) -> int:
        return len(self._queue)

    def __iter__(self):
        return iter(self._queue)

    def __getitem__(self, index: int) -> Any:
        return self._queue[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self._queue[index] = value

    def __delitem__(self, index: int) -> None:
        del self._queue[index]

    def __contains__(self, value: Any) -> bool:
        return value in self._queue


class Stack:
    """A simple class that creates a stack of values to be processed in order. Can be called to get the next value in
    the stack or to add a value to the stack if an argument is passed. Functionally identical to the Queue class but
    with a different order of processing.

    Methods:
        add(value: Any) -> None:
            Add a value to the top of the stack.
        pop() -> Any | None:
            Remove and return the next value in the stack.
        peek() -> Any | None:
            Return the next value in the stack without removing it.
        insert(value: Any, distance: int = 0) -> None:
            Insert a value into the stack at a specified distance from the top of the stack. (Or bottom if negative.)
        remove(value: Any) -> None:
            Remove a value from the stack. Note that this will remove all instances of the value.
        remove_at(index: int) -> None:
            Remove a value from the stack at a specified index.
        index(value: Any, instance: int = 0) -> int | None:
            Return the first index of a value in the stack.
    """

    def __init__(self, values: list[Any] | None = None) -> None:
        """Initialize the Stack object.

        Args:
            values (list[Any] | None, optional):
                The values to add to the stack.
                Defaults to [] if None.
        """
        if values is None:
            values = []
        self._stack = values

    @property
    def stack(self) -> list[Any]:
        return self._stack

    @stack.setter
    def stack(self, values: list[Any]) -> None:
        self._stack = values

    @stack.deleter
    def stack(self) -> None:
        self._stack.clear()

    def add(self, value: Any) -> None:
        """Add a value to the top of the stack.

        Args:
            value (Any):
                The value to add to the top of the stack.
        """
        self._stack.append(value)

    def insert(self, value: Any, distance: int = 0) -> None:
        """Insert a value into the stack at a specified distance from the top of the stack. (Or bottom if negative.)

        Args:
            value (Any):
                The value to insert into the stack.
            distance (int, optional):
                The distance from the top of the stack to insert the value.
                Defaults to 0.
        """
        self._stack.insert(-distance - 1, value)

    def pop(self, distance: int = 0) -> Any | None:
        """Remove and return the next value in the stack.

        Args:
            distance (int, optional):
                The distance from the top of the stack to pop the value.
                Defaults to 0.

        Returns:
            Any: The next value in the stack.
            None: If the stack is empty.
        """
        # If the distance is positive, pop from the top of the stack. If negative, flip it to pop from the bottom of
        # the stack.
        flipped_distance = -distance - 1
        # If the distance is out of bounds, return None. This also catches the case where the stack is empty.
        if flipped_distance >= len(self._stack) or abs(flipped_distance) > len(self._stack):
            return None

        return self._stack.pop(flipped_distance) if self._stack else None

    def peek(self, distance: int = 0) -> Any | None:
        """Return the next value in the stack without removing it.

        Args:
            distance (int, optional):
                The distance from the top of the stack to peek at.
                Defaults to 0.

        Returns:
            Any: The next value in the stack.
            None: If the stack is empty or the distance is out of bounds.
        """
        # If the distance is positive, peek from the top of the stack. If negative, flip it to peek from the bottom of
        # the stack.
        flipped_distance = -distance - 1
        # If the distance is out of bounds, return None. This also catches the case where the stack is empty.
        if flipped_distance >= len(self._stack) or abs(flipped_distance) > len(self._stack):
            return None

        return self._stack[flipped_distance]

    def remove(self, value: Any) -> None:
        """Remove a value from the stack. Note that this will remove all instances of the value.

        Args:
            value (Any):
                The value to remove from the stack.
        """
        self._stack = [item for item in self._stack if item != value]

    def remove_at(self, index: int) -> None:
        """Remove a value from the stack at a specified index.

        Args:
            index (int):
                The distance from the top of the stack to remove the value.
        """
        flipped_index = -index - 1
        del self._stack[flipped_index]

    def index(self, value: Any, instance: int = 0) -> int | None:
        """Return the first index of a value in the stack.

        Args:
            value (Any):
                The value to find the index of.
            instance (int, optional):
                The instance of the value to find the index of.
                Defaults to 0. (The first instance.)

        Returns:
            int: The index of the value.
            None: If the value is not in the stack or the instance is out of bounds.
        """
        instances = [i for i, item in enumerate(self._stack[::-1]) if item == value]

        # If the instance of the value is not in the stack, return None.
        if instance >= len(instances) or abs(instance) > len(instances):
            return None

        return instances[instance]

    def __len__(self) -> int:
        return len(self._stack)

    def __repr__(self) -> str:
        return str(self._stack[-1] if self._stack else None)

    def __bool__(self) -> bool:
        return bool(self._stack)

    def __call__(self, value: Any = None) -> Any:
        if value is not None:
            self._stack.append(value)
            return None

        return self._stack.pop() if self._stack else None

    def __iter__(self):
        return iter(self._stack)

    def __getitem__(self, index: int) -> Any:
        return self._stack[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self._stack[index] = value

    def __delitem__(self, index: int) -> None:
        del self._stack[index]

    def __contains__(self, value: Any) -> bool:
        return value in self._stack


class PriorityQueue:
    """A simple class that creates a priority queue of values to be processed in order. Can be called to get the next
    value in the queue or to add a value to the queue if an argument and priority are passed. Similar to the Queue
    class, but with the ability to prioritize values. The value with the highest priority will be processed first.

    Properties:
        queue (list[dict[str, Any | float]]):

    Methods:
        add(value: Any, priority: float) -> None:
            Add a value to the queue with a specified priority.
        pop() -> Any | None:
            Remove and return the next value in the queue.
        peek() -> Any | None:
            Return the next value in the queue without removing it.
        clear() -> None:
            Clear the priority queue.
        remove(value: Any, quantity: int = 1) -> None:
            Remove a value from the priority queue.
        remove_at(index: int) -> None:
            Remove a value from the priority queue at a specified index.
        index(value: Any, instance: int = 0) -> int | None:
            Return the first index of a value in the priority queue.
    """

    def __init__(self, values: list[dict[str, Any | float]] | None = None) -> None:
        """Initialize the PriorityQueue object.

        Args:
            values (list[dict[str, Any | float]] | None, optional):
                The values to add to the priority queue.
                Defaults to [] if None.
        """
        if values is None:
            values = []

        self._priority_queue: list[dict[str, Any | float]] = values

    @property
    def queue(self) -> list[dict[str, Any | float]]:
        return self._priority_queue

    @queue.setter
    def queue(self, values: list[dict[str, Any | float]]) -> None:
        self._priority_queue = values
        self._sort_queue()

    @queue.deleter
    def queue(self) -> None:
        self._priority_queue.clear()

    def add(self, value: Any, priority: float = 0) -> None:
        """Add a value to the queue with a specified priority.

        Args:
            value (Any):
                The value to add to the queue.
            priority (float, optional):
                The priority of the value.
                Defaults to 0.
        """
        item = {"value": value, "priority": priority}
        self._priority_queue.append(item)

    def pop(self) -> Any | None:
        """Remove and return the next value in the queue.

        Returns:
            Any: The next value in the queue.
            None: If the queue is empty.
        """
        if not self._priority_queue:
            return None

        self._sort_queue()

        return self._priority_queue.pop(0)["value"]

    def _sort_queue(self) -> None:
        """Sort the queue by priority."""
        self._priority_queue.sort(key=lambda x: x["priority"], reverse=True)

    def peek(self) -> Any | None:
        """Return the next value in the queue without removing it.

        Returns:
            Any: The next value in the queue.
            None: If the queue is empty.
        """
        if not self._priority_queue:
            return None

        self._sort_queue()

        return self._priority_queue[0]["value"]

    def clear(self) -> None:
        """Clear the priority queue."""
        self._priority_queue.clear()

    def remove(self, value: Any, quantity: int = 1) -> None:
        """Remove a value from the priority queue.

        Args:
            value (Any):
                The value to remove from the priority queue.
            quantity (int, optional):
                The number of instances of the value to remove. Set to -1 to remove all instances.
                Defaults to 1.
        """
        if quantity == -1:
            self._priority_queue = [item for item in self._priority_queue if item["value"] != value]
            return

        for _ in range(quantity):
            index = self.index(value)

            if index is not None:
                del self._priority_queue[index]
            else:
                return

    def remove_at(self, index: int) -> None:
        """Remove a value from the priority queue at a specified index.

        Args:
            index (int):
                The index of the value to remove from the priority queue.
        """
        del self._priority_queue[index]

    def index(self, value: Any, instance: int = 0) -> int | None:
        """Return the first index of a value in the priority queue.

        Args:
            value (Any):
                The value to find the index of.
            instance (int, optional):
                The instance of the value to find the index of.
                Defaults to 0. (The first instance.)

        Returns:
            int: The index of the value.
            None: If the value is not in the priority queue or the instance is out of bounds.
        """
        instances = [i for i, item in enumerate(self._priority_queue) if item["value"] == value]

        # If the instance of the value is not in the queue, return None.
        if instance >= len(instances) or abs(instance) > len(instances):
            return None

        return instances[instance]

    def priority(self, value: Any, priority: float, instance: int = 0) -> None:
        """Change the priority of a value in the priority queue.

        Args:
            value (Any):
                The value to change the priority of.
            priority (float):
                The new priority of the value.
            instance (int, optional):
                The instance of the value to change the priority of.
                Defaults to 0. (The first instance.)
        """
        index = self.index(value, instance)

        if index is not None:
            self._priority_queue[index]["priority"] = priority

    def get_priority(self, value: Any, instance: int = 0) -> float | None:
        """Return the priority of a value in the priority queue.

        Args:
            value (Any):
                The value to get the priority of.
            instance (int, optional):
                The instance of the value to get the priority of.
                Defaults to 0. (The first instance.)

        Returns:
            float: The priority of the value.
            None: If the value is not in the priority queue or the instance is out of bounds.
        """
        index = self.index(value, instance)

        if index is not None:
            return self._priority_queue[index]["priority"]

        return None

    @property
    def highest_priority(self) -> float | None:
        """Return the highest priority in the priority queue.

        Returns:
            float: The highest priority in the priority queue.
            None: If the priority queue is empty.
        """
        if not self._priority_queue:
            return None

        return self._priority_queue[0]["priority"]

    @property
    def lowest_priority(self) -> float | None:
        """Return the lowest priority in the priority queue.

        Returns:
            float: The lowest priority in the priority queue.
            None: If the priority queue is empty.
        """
        if not self._priority_queue:
            return None

        return self._priority_queue[-1]["priority"]

    @property
    def average_priority(self) -> float | None:
        """Return the average priority in the priority queue.

        Returns:
            float: The average priority in the priority queue.
            None: If the priority queue is empty.
        """
        if not self._priority_queue:
            return None

        return sum(item["priority"] for item in self._priority_queue) / len(self._priority_queue)

    @property
    def median_priority(self) -> float | None:
        """Return the median priority in the priority queue.

        Returns:
            float: The median priority in the priority queue.
            None: If the priority queue is empty.
        """
        if not self._priority_queue:
            return None

        sorted_queue = sorted(item["priority"] for item in self._priority_queue)
        length = len(sorted_queue)
        half = length // 2

        if length % 2 == 0:
            return (sorted_queue[half - 1] + sorted_queue[half]) / 2

        return sorted_queue[half]

    def __repr__(self) -> str:
        return str(self._priority_queue[0]["value"] if self._priority_queue else None)

    def __bool__(self) -> bool:
        return bool(self._priority_queue)

    def __call__(self, value: Any = None, priority: float = 0) -> Any:
        if value is not None:
            self._priority_queue.append({"value": value, "priority": priority})
            return None

        return self.pop()

    def __len__(self) -> int:
        return len(self._priority_queue)

    def __iter__(self):
        return iter(self._priority_queue)

    def __getitem__(self, index: int) -> Any:
        return self._priority_queue[index]["value"]

    def __setitem__(self, index: int, value: Any) -> None:
        self._priority_queue[index]["value"] = value

    def __delitem__(self, index: int) -> None:
        del self._priority_queue[index]

    def __contains__(self, value: Any) -> bool:
        return any(item["value"] == value for item in self._priority_queue)


if __name__ == "__main__":
    # Queue
    print("Queue")
    queue = Queue([1, 2, 3, 4, 5])
    print(queue.queue)
    queue.add(6)
    print(queue.queue)
    print(queue.pop(), "Expected: 1")
    print(queue.queue)
    print(queue.peek(), "Expected: 2")
    print(queue.queue)
    queue.insert(7, 2)
    print(queue.queue)
    queue.remove(3)
    print(queue.queue)
    queue.remove_at(1)
    print(queue.queue)
    print(queue.index(5), "Expected: 2")
    print(queue.index(5, 1), "Expected: None")
    print(queue.index(5, -1), "Expected: 2")
    print(queue.index(5, -2), "Expected: None")
    print(queue.index(3), "Expected: None")
    print(queue.index(3, -1), "Expected: None")

    # Stack
    print("\nStack")
    stack = Stack([1, 2, 3, 4, 5])
    print(stack.stack)
    stack.add(6)
    print(stack.stack, "Expected: [1, 2, 3, 4, 5, 6]")
    print(stack.pop(), "Expected: 6")
    print(stack.stack, "Expected: [1, 2, 3, 4, 5]")
    print(stack.peek(), "Expected: 5")
    print(stack.stack, "Expected: [1, 2, 3, 4, 5]")
    stack.insert(7, 2)
    print(stack.stack, "Expected: [1, 2, 7, 3, 4, 5]")
    stack.remove(3)
    print(stack.stack, "Expected: [1, 2, 7, 4, 5]")
    stack.remove_at(1)
    print(stack.stack, "Expected: [1, 2, 7, 5]")
    print(stack.index(5), "Expected: 0")
    print(stack.index(5, 1), "Expected: None")
    print(stack.index(5, -1), "Expected: 0")
    print(stack.index(5, -2), "Expected: None")
    print(stack.index(3), "Expected: None")
    print(stack.index(3, -1), "Expected: None")

    # PriorityQueue
    print("\nPriorityQueue")
    priority_queue = PriorityQueue([{"value": 1, "priority": 1}, {"value": 2, "priority": 2},
                                   {"value": 3, "priority": 3}, {"value": 4, "priority": 4},
                                   {"value": 5, "priority": 5}])
    print(priority_queue.queue)
    priority_queue.add(6, 6)
    print(priority_queue.queue)
    print(priority_queue.pop(), "Expected: 6")
    print(priority_queue.queue)
    print(priority_queue.peek(), "Expected: 5")
    print(priority_queue.queue)
    print(priority_queue.average_priority, "Expected: 3.0")
    print(priority_queue.highest_priority, "Expected: 5.0")
    print(priority_queue.lowest_priority, "Expected: 1.0")
    print(priority_queue.median_priority, "Expected: 3.0")
    priority_queue.remove(3)
    print(priority_queue.queue)
    priority_queue.remove_at(1)
    print(priority_queue.queue)
    print(priority_queue.index(5), "Expected: 0")
    print(priority_queue.index(5, 1), "Expected: None")
    print(priority_queue.index(5, -1), "Expected: 0")
    print(priority_queue.index(5, -2), "Expected: None")
    print(priority_queue.index(3), "Expected: None")
    print(priority_queue.index(3, -1), "Expected: None")
    priority_queue.priority(5, 0)
    print(priority_queue.queue)
    print(priority_queue.get_priority(5), "Expected: 0.0")
    print(priority_queue.get_priority(5, 1), "Expected: None")
    print(priority_queue.get_priority(5, -1), "Expected: 0.0")
    print(priority_queue.get_priority(5, -2), "Expected: None")
    print(priority_queue.get_priority(3), "Expected: None")
    print(priority_queue.get_priority(3, -1), "Expected: None")
    priority_queue.clear()
    print(priority_queue.queue)


