
class AbstractReader(object):
    """Wraps a file handler and provides access to stats contents"""

    def __init__(self, filepath, CLASSES, auto_close, header):
        """Constructs the read only file handler"""
        self.header = header
        self.CLASSES = CLASSES
        self.handler = open(filepath, 'r')
        self.process_file()

        if auto_close:
            self.close()

    def __iter__(self):
        self.handler.seek(0) # Reset the file pointer
        return self.handler

    def close(self):
        """Close the file handler"""
        self.handler.close()

    def get_data(self):
        raise NotImplementedError

    def process_line(self, line):
        raise NotImplementedError

    def process_file(self):
        """Calls process_line for each line in input file"""

        # Skip Header
        for i in range(0,1):
            self.handler.readline()

        for line in self.handler:
            self.process_line(line.strip())

