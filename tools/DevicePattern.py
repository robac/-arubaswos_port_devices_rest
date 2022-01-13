import re
from .exceptions import *

class DevicePattern:
    def __init__(self):
        self.patterns = {}

    def add_pattern(self, name, pattern):
        if name not in pattern:
            self.patterns[name] = {}
        self.patterns[name]['pattern'] = pattern
        self.patterns[name]['compiled'] = re.compile(pattern)

    def get_pattern(self, name):
        if name not in self.patterns:
            raise NonExistentPattern
        else:
            return self.patterns[name]['pattern']

    def get_pattern_compiled(self, name):
        if name not in self.patterns:
            raise NonExistentPattern
        else:
            return self.patterns[name]['compiled']
