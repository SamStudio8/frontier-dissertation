from Frontier.frontier import classify_label, encode_class
from Frontier.IO.AbstractReader import AbstractReader

class AQCReader(AbstractReader):

    def __init__(self, filepath, CLASSES=None, auto_close=True):
        self.targets = {}
        super(AQCReader, self).__init__(filepath, CLASSES, auto_close, 1)

    def process_line(self, line):
        fields = line.split("\t")

        _id = fields[0]
        if self.CLASSES is None:
            _class = fields[4]
            _code = _class
        else:
            _class = classify_label(self.CLASSES, fields[4])
            _code = encode_class(self.CLASSES, _class)

        self.targets[_id] = _code

    def get_data(self):
        return self.targets

