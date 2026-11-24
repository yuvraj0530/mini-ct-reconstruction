
import pytest

from ds.scan_queue import ScanQueue


def test_new_queue_is_empty():
    queue = ScanQueue()

    assert queue.is_empty() is True
    assert queue.size() == 0


def test_enqueue_request():
    queue = ScanQueue()

    queue.enqueue("Scan A")

    assert queue.size() == 1
    assert queue.is_empty() is False


def test_dequeue_request():
    queue = ScanQueue()

    queue.enqueue("Scan A")
    queue.enqueue("Scan B")

    result = queue.dequeue()

    assert result == "Scan A"
    assert queue.size() == 1


def test_fifo_order():
    queue = ScanQueue()

    queue.enqueue("Scan A")
    queue.enqueue("Scan B")
    queue.enqueue("Scan C")

    assert queue.dequeue() == "Scan A"
    assert queue.dequeue() == "Scan B"
    assert queue.dequeue() == "Scan C"


def test_peek_request():
    queue = ScanQueue()

    queue.enqueue("Scan A")
    queue.enqueue("Scan B")

    result = queue.peek()

    assert result == "Scan A"
    assert queue.size() == 2


def test_dequeue_empty_queue():
    queue = ScanQueue()

    with pytest.raises(IndexError):
        queue.dequeue()


def test_peek_empty_queue():
    queue = ScanQueue()

    with pytest.raises(IndexError):
        queue.peek()


def test_enqueue_none():
    queue = ScanQueue()

    with pytest.raises(ValueError):
        queue.enqueue(None)


def test_clear_queue():
    queue = ScanQueue()

    queue.enqueue("Scan A")
    queue.enqueue("Scan B")

    queue.clear()

    assert queue.is_empty() is True
    assert queue.size() == 0


def test_queue_after_multiple_operations():
    queue = ScanQueue()

    queue.enqueue("Scan A")
    queue.enqueue("Scan B")
    queue.dequeue()
    queue.enqueue("Scan C")

    assert queue.peek() == "Scan B"
    assert queue.size() == 2
