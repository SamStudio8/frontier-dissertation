from Frontier.frontier import classify_label, encode_class

class AQCReader(object):

    def __init__(self, filepath, CLASSES, auto_close=False):
        """Constructs the read only file handler"""
        self.handler = open(filepath, 'r')
        self.handler.seek(0)
        self.targets = {}

        self.process_file(CLASSES)

        if auto_close:
            self.close()

    def process_file(self, CLASSES):
        """Parse lines in to dict"""
        self.handler.readline() # Skip header
        for uline in self.handler:
            line = uline.strip()
            fields = line.split("\t")

            _id = fields[0]
            _class = classify_label(CLASSES, fields[4])
            _code = encode_class(CLASSES, _class)

            self.targets[_id] = _code

    def get_targets(self):
        return self.targets

    def close(self):
        """Close the file handler"""
        self.handler.close()

    def __iter__(self):
        self.handler.seek(0) # Reset the file pointer
        return self.handler
