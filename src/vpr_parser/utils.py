import time


class Timer:
    def __init__(self, name: str):
        self.name = name
        self.start_time = time.time()
        self.end_time = time.time()
        self.parts = []

    def _get_proper_unit(self, number: float):
        if number >= 1:
            return "s", 1
        elif number >= 0.001:
            return "ms", 1000
        elif number >= 0.000001:
            return "μs", 1000000
        else:
            return "ns", 1000000000

    def _add_proper_unit(self, number: float) -> str:
        unit, multiplier = self._get_proper_unit(number)
        return f"{number * multiplier:.2f} {unit}"

    def add_part(self, name: str) -> None:
        self.parts.append((name, time.time()))

    def end(self, name: str):
        self.end_time = time.time()
        self.parts.append((name, self.end_time))

    def as_dict(self) -> dict:
        parts = []
        last_time = self.start_time
        for name, current_time in self.parts:
            parts.append({"name": name, "duration": current_time - last_time})
            last_time = current_time
        return {
            "name": self.name,
            "duration": self.end_time - self.start_time,
            "parts": parts,
        }

    def as_human_readable(self) -> str:
        data = self.as_dict()
        report = f'Task "{self.name}" took ' + self._add_proper_unit(data["duration"])
        if data["parts"]:
            report += " = "
        for part in data["parts"]:
            report += f"{self._add_proper_unit(part['duration'])}({part['name']}) + "
        if data["parts"]:
            report = report[:-3]
        return report
