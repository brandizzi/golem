from copy import deepcopy
from collections import Sequence

from lxml.etree import fromstring, tostring
from lxml import cssselect  

class Animator(object):
    def __init__(self, template):
        self.template = template
        self.values = {}

    def fill(self, selector, value):
        self.values[selector] = value

    def result(self):
        tree = fromstring(self.template)
        for key in self.values:
            self.replace_first_text_element(tree, key)
            
        return tostring(tree)

    def replace_first_text_element(self, tree, selector_string):
        selector = cssselect.CSSSelector(selector_string)
        elements = selector(tree)
        value = self.values[selector_string]
        if isinstance(value, basestring):
            for element in elements:
                element.text = self.values[selector_string]
        elif isinstance(value, Sequence):
            parents = set([element.getparent() for element in elements])
            for parent in parents:
                children = [element for element in elements if element in parent]
                for child in children:
                    parent.remove(child)
                for item in value:
                    element = deepcopy(elements[0])
                    element.text = item
                    parent.append(element)
                    
