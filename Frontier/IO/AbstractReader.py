__author__ = "Sam Nicholls <sn8@sanger.ac.uk>"
__copyright__ = "Copyright (c) Sam Nicholls"
__version__ = "0.1.0"
__maintainer__ = "Sam Nicholls <sam@samnicholls.net>"

class AbstractReader(object):
    """Wraps a file handler and provides controlled access to its contents."""

    def __init__(self, filepath, CLASSES, auto_close, header):
        """Constructs the read only file handler."""
        self.header = header
        self.CLASSES = CLASSES

        if not filepath:
            raise IOError("You must specify a file.")

        self.handler = open(filepath, 'r')
        self.process_file()

        if auto_close:
            self.close()

    def __iter__(self):
        """Reset the file pointer and return an iterable."""
        self.handler.seek(0)
        return self.handler

    def close(self):
        """Close the file handler."""
        #TODO Check file is not already closed...
        self.handler.close()

    def get_data(self):
        """Return read data."""
        raise NotImplementedError("get_data has not been implemented")

    def process_line(self, line):
        """Process a record of the input file."""
        raise NotImplementedError("process_line has not been implemented")

    def process_file(self):
        """Calls process_line for each line in input file."""

        # Skip Header
        for i in range(0,self.header):
            self.handler.readline()

        for line in self.handler:
            self.process_line(line.strip())

