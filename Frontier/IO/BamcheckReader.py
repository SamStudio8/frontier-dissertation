__author__ = "Sam Nicholls <sn8@sanger.ac.uk>"
__copyright__ = "Copyright (c) Sam Nicholls"
__version__ = "0.1.0"
__maintainer__ = "Sam Nicholls <sam@samnicholls.net>"

from Frontier.IO.AbstractReader import AbstractReader

def tidy_key(key):
    """Sanitize summary number key."""
    key = key[:-1].replace(" ", "-")
    key = key.replace(".", "-")
    key = key.replace("_", "-")
    return key.strip()

class BamcheckReader(AbstractReader):
    """Wraps a file handler and provides access to bamcheckr'd file contents."""

    def __init__(self, filepath, CLASSES, auto_close=True):
        """Initialise the structures for storing data and construct the reader."""
        self.summary = SummaryNumbers()
        self.indel = IndelDistribution()
        super(BamcheckReader, self).__init__(filepath, CLASSES, auto_close, 0)

    def process_line(self, line):
        """Process a record of the bamcheckr'd file."""
        if line[0] == "#":
            # Skip comments
            return
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
                return
            self.summary[name] = value

        elif fields[0] == "ID":
            self.indel.lengths.append(int(fields[1]))
            self.indel.inserts.append(int(fields[2]))
            self.indel.deletes.append(int(fields[3]))

    def get_data(self):
        """Return read summary data."""
        return self.summary


class SummaryNumbers(dict):
    """Wraps a dictionary and provides functionality to search for keys."""
    def __init__(self, *args):
        dict.__init__(self, args)

    def search(self, query):
        """Search the structure for keys matching a given query."""
        matches = []
        for key in self:
            if query.lower() in key.lower():
                matches.append(key)
        return matches

class IndelDistribution(object):
    """Novel object to hold a trio of lengths, inserts and deletes counters."""
    def __init__(self):
        self.lengths = []
        self.inserts = []
        self.deletes = []

    def total_inserts(self):
        """Return sum of total inserts."""
        return sum(self.inserts)

    def total_deletes(self):
        """Return sum of total deletes."""
        return sum(self.deletes)
