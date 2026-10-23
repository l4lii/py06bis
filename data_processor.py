from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._queue: list[str] = []
        self._count: int = 0

    def output(self) -> tuple[int, str]:
        if not self._queue:
            raise ValueError("No data available")
        value = self._queue.pop(0)
        rank = self._count
        self._count += 1
        return (rank, value)

    @abstractmethod
    def validate(self, data: Any) -> bool: pass
    @abstractmethod
    def ingest(self, data: Any) -> None: pass


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            if not data:
                return (False)
            for item in data:
                if isinstance(item, bool):
                    return (False)
                if not isinstance(item, (int, float)):
                    return (False)
            return (True)
        return (isinstance(data, (int, float)) and not isinstance(data, bool))

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._queue.append(str(item))
        else:
            self._queue.append(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            if not data:
                return (False)
            for item in data:
                if not isinstance(item, str):
                    return (False)
            return (True)
        return (isinstance(data, str))

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._queue.append(item)
        else:
            self._queue.append(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            if not data:
                return (False)
            for item in data:
                if not self.validate(item):
                    return (False)
        else:
            if not isinstance(data, dict):
                return (False)
            if not set(data.keys()) == {"log_level", "log_message"}:
                return (False)
            if not isinstance(data["log_level"], str):
                return (False)
            if not isinstance(data["log_message"], str):
                return (False)
        return (True)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            for item in data:
                line = item["log_level"] + ": " + item["log_message"]
                self._queue.append(line)
        else:
            line = data["log_level"] + ": " + data["log_message"]
            self._queue.append(line)


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")
    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")
    except ValueError as e:
        print("Got exception:", e)
    print("Processing data: [1, 2, 3, 4, 5]")
    numeric.ingest([1, 2, 3, 4, 5])
    print("Extracting 3 values...")
    for i in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")
    print("Testing Text Processor...")
    text = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")
    print(f"Trying to validate input 'Hello': {text.validate('Hello')}")
    print("Processing data: ['Hello', 'Nexus', 'World']")
    text.ingest(['Hello', 'Nexus', 'World'])
    print("Extracting 1 value...")
    for i in range(1):
        rank, value = text.output()
        print(f"Text value {rank}: {value}")
    print("Testing Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    logs: list[dict[str, str]] = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]
    print(f"Processing data: {logs}")
    log.ingest(logs)
    print("Extracting 2 values...")
    for i in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")
