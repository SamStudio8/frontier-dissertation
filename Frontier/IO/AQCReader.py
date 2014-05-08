__author__ = "Sam Nicholls <sn8@sanger.ac.uk>"
__copyright__ = "Copyright (c) Sam Nicholls"
__version__ = "0.1.0"
__maintainer__ = "Sam Nicholls <sam@samnicholls.net>"

from Frontier.frontier import classify_label, encode_class
from Frontier.IO.AbstractReader import AbstractReader

class AQCReader(AbstractReader):
    """Wraps a file handler and provides access to AQC matrix contents."""

    def __init__(self, filepath, CLASSES=None, auto_close=True):
        """Initialise the structures for storing data and construct the reader."""
        self.targets = {}
        super(AQCReader, self).__init__(filepath, CLASSES, auto_close, 1)

    def process_line(self, line):
        """Process a record of the AQC matrix file."""
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
        """Return the targets structure."""
        return self.targets

