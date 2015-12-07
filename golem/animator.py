import xml.etree.ElementTree as ET

from collections import defaultdict

class Animator(object):

    def __init__(self, document, parser=ET):
        self.parser = parser
        self.document = self.parser.fromstring(document)
        self.class_map = defaultdict(list)
        for element in self.document.iter():
            if 'class' in element.attrib:
                classes = element.attrib['class'].split()
                for c in classes:
                    self.class_map[c].append(element)

    def find(self, class_=None):
        return self.class_map[class_]

    def tostring(self):
        return self.parser.tostring(self.document)
