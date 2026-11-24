
from collections import deque


class ScanQueue:
    """FIFO queue for managing CT scan requests."""

    def __init__(self):
        self._queue = deque()

    def enqueue(self, scan_request):
        """Add a scan request to the rear of the queue."""

        if scan_request is None:
            raise ValueError("Scan request cannot be None.")

        self._queue.append(scan_request)

    def dequeue(self):
        """Remove and return the oldest scan request."""

        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")

        return self._queue.popleft()

    def peek(self):
        """Return the next scan request without removing it."""

        if self.is_empty():
            raise IndexError("Cannot peek into an empty queue.")

        return self._queue[0]

    def is_empty(self):
        """Check whether the queue is empty."""

        return len(self._queue) == 0

    def size(self):
        """Return the number of scan requests."""

        return len(self._queue)

    def clear(self):
        """Remove all scan requests."""

        self._queue.clear()
