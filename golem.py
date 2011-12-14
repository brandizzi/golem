from copy import deepcopy
from collections import Sequence
from itertools import product

from lxml.etree import fromstring, tostring
from lxml import cssselect  

class Animator(object):
    def __init__(self, template):
        self.template = template
        self.values = {}
        self.attribute_dicts = {}
        self.fillers = {}

    def fill(self, selector, content=None, **attributes):
        self.values[selector] = content
        self.attribute_dicts[selector] = attributes

    def fillSubelements(self, selector, objects, fillers):
        self.fillers[selector] = (objects, fillers)

    def result(self):
        tree = fromstring(self.template)
        for key in self.values:
            self.replace_first_text_element(tree, key)
        for key in self.attribute_dicts:
            self.set_attributes_values(tree, key)
        for key in self.fillers:
            self.apply_fillers(tree, key)

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

    def set_attributes_values(self, tree, selector_string):
        selector = cssselect.CSSSelector(selector_string)
        elements = selector(tree)
        attributes = self.attribute_dicts[selector_string]
        for element in elements:
            for attribute, value in attributes.items():
                element.set(attribute, value)

    def apply_fillers(self, tree, selector_string):
        selector = cssselect.CSSSelector(selector_string)
        elements = selector(tree)
        objects, fillers = self.fillers[selector_string]
        for root in elements:
            self.apply_fillers_to_subelements(root, objects, fillers)

    def apply_fillers_to_subelements(self, root, objects, fillers):
        parents = {}
        to_remove = set()
        for filler in fillers:
            selector = cssselect.CSSSelector(filler.selector_string)
            subelements = selector(root)
            for subelement in subelements:
                parent = self.get_parent_until_root(subelement, root)
                to_remove.add(parent)
            for obj in objects:
                key = id(obj), filler.selector_string
                if not subelements: continue
                parent = self.get_parent_until_root(subelements[0], root)
                if key not in parents:
                    parents[key] = parent
        for removing in to_remove:
            root.remove(removing)
        for obj in objects:
            for filler in fillers:
                element = parents.get((id(obj), filler.selector_string))
                if element is None: continue
                selector = cssselect.CSSSelector(filler.selector_string)
                subelements = selector(element)
                for subelement in subelements:
                    if filler.value:
                        subelement.text = str(filler.value(obj))
                    for attribute, func in filler.attributes.items():
                        subelement.set(attribute, str(func(obj)))
            root.append(deepcopy(element))

    def get_parent_until_root(self, subelement, root):
        if subelement.getparent() == root:
            return subelement
        else:
            return self.get_parent_until_root(subelement.getparent(), root)
        

nop = lambda _ : ""

class Filler(object):
    def __init__(self, selector_string, text_func=None, **attributes):
        self.selector_string = selector_string
        self.value = text_func
        self.attributes = attributes

