from abc import ABC, abstractmethod
from typing import Any, Protocol


class DataProcessor(ABC):
    name: str = "Processor"

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
    name: str = "Numeric Processor"

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
    name: str = "Text Processor"

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
    name: str = "Log Processor"

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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class CSVExportPlugin():
    def process_output(self, data: list[tuple[int, str]]) -> None:
        texts: list[str] = []
        for couple in data:
            texts.append(couple[1])
        print("CSV Output:")
        print(",".join(texts))


class JSONExportPlugin():
    def process_output(self, data: list[tuple[int, str]]) -> None:
        items: list[str] = []
        for couple in data:
            items.append(f'"item_{couple[0]}": "{couple[1]}"')
        print("JSON Output:")
        print(f'{{{", ".join(items)}}}')


class DataStream():
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            _handled = False
            for proc in self._processors:
                if proc.validate(item):
                    proc.ingest(item)
                    _handled = True
                    break
            if _handled is False:
                print(
                    "DataStream error - "
                    "Can't process element in stream:", f"{item}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
        else:
            for proc in self._processors:
                print(f"{proc.name}: total "
                      f"{len(proc._queue) + proc._count} items processed, "
                      f"remaining {len(proc._queue)} on processor")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            batch: list[tuple[int, str]] = []
            for _ in range(nb):
                if not proc._queue:
                    break
                batch.append(proc.output())
            plugin.process_output(batch)


if __name__ == "__main__":
    stream = DataStream()
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")
    stream.print_processors_stats()
    print("Registering Processors")
    numeric = NumericProcessor()
    stream.register_processor(numeric)
    text = TextProcessor()
    stream.register_processor(text)
    log = LogProcessor()
    stream.register_processor(log)
    batch: list[Any] = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {
                'log_level': 'WARNING',
                'log_message': 'Telnet access! Use ssh instead'
            },
            {
                'log_level': 'INFO',
                'log_message': 'User wil is connected'
            }
        ],
        42, ['Hi', 'five']
    ]
    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()
    print("Send 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExportPlugin())
    stream.print_processors_stats()
