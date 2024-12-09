import time

class Benchmarker:
    def __init__(self, name="unnamed"):
        self.name = name
        self.benchmarks = {}

    def get_time(self):
        # Returns the current time in seconds
        return time.time()

    def start(self, name):
        # Create benchmark record and assign start time
        record = {}
        record['start'] = self.get_time()
        self.benchmarks[name] = record

    def end(self, name):
        # Retrieve benchmark record and assign end time
        record = self.benchmarks.get(name)
        if record is not None:
            record['end'] = self.get_time()
            record['duration'] = record['end'] - record['start']

    def duration(self, name):
        # Return the duration of a benchmark record
        record = self.benchmarks.get(name)
        if record is not None:
            return record.get('duration')
        return None

    def summary(self):
        # Returns a string summary of the benchmarks
        output = f"BENCHMARK [{self.name}]\n"
        for benchmark_name, record in self.benchmarks.items():
            duration = record.get('duration')
            output += f"\t{benchmark_name} -> {duration}\n"
        return output
