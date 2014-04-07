"""Read from a samtools stats file"""

__author__ = "Sam Nicholls <sn8@sanger.ac.uk>"
__copyright__ = "Copyright (c) Sam Nicholls"
__version__ = "0.0.1"
__maintainer__ = "Sam Nicholls <sam@samnicholls.net>"

def tidy_key(key):
    key = key[:-1].replace(" ", "-")
    key = key.replace(".", "-")
    key = key.replace("_", "-")
    return key.strip()

class BamcheckReader(object):
    """Wraps a file handler and provides access to stats contents"""

    def __init__(self, filepath, CLASSES, auto_close=False):
        """Constructs the read only file handler and parses the header"""
        self.summary = SummaryNumbers()
        self.indel = IndelDistribution()

        self.handler = open(filepath, 'r')
        self.handler.seek(0)
        self.process_file()

        if auto_close:
            self.close()

    def process_file(self):
        """Parse lines in to dict"""
        for uline in self.handler:
            line = uline.strip()
            if line[0] == "#":
                # Skip comments
                continue
            fields = line.split("\t")
            if fields[0] == "SN":
                name = tidy_key(fields[1])
                try:
                    value = float(fields[2])
                except ValueError:
                    value = fields[2]

                # Check whether key already exists in summary
                if name in self.summary:
                    print "[NOTE] Duplicate key for %s found in %s" % (name, self.handler.name)

                    # Check whether the duplicate value is equal to the current
                    if self.summary[name] != value:
                        raise Exception("[FAIL] Duplicate differing key for %s found in %s" % (name, self.handler.name))
                    continue
                self.summary[name] = value

            elif fields[0] == "ID":
                self.indel.lengths.append(int(fields[1]))
                self.indel.inserts.append(int(fields[2]))
                self.indel.deletes.append(int(fields[3]))

    def close(self):
        """Close the file handler"""
        self.handler.close()

    def __iter__(self):
        self.handler.seek(0) # Reset the file pointer
        return self.handler


class SummaryNumbers(dict):
    def __init__(self, *args):
        dict.__init__(self, args)

    def search(self, query):
        matches = []
        for key in self:
            if query.lower() in key.lower():
                matches.append(key)
        return matches

class IndelDistribution(object):

    def __init__(self):
        self.lengths = []
        self.inserts = []
        self.deletes = []

    def total_inserts(self):
        return sum(self.inserts)

    def total_deletes(self):
        return sum(self.deletes)
