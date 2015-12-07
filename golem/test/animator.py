import unittest

from golem.animator import Animator

class TestAnimator(unittest.TestCase):

    def test_find_by_class(self):
        """
        Animator should provide a way to find elements by class.
        """
        document = """
        <html>
            <body>
                <div class="c1">Text 1</div>
                <div class="c2">Text 2</div>
                <div class="c1">Text 3</div>
            </body>
        </html>
        """
        animator = Animator(document)
        divs = animator.find(class_='c1')

        self.assertEquals(2, len(divs))
        self.assertEquals('Text 1', divs[0].text)
        self.assertEquals('Text 3', divs[1].text)

    def test_tostring(self):
        """
        Animator should have a ``tostring()`` method to return its document
        as a string again.
        """
        document = """
        <html>
            <body>
                <div class="c1">Text 1</div>
                <div class="c2">Text 2</div>
                <div class="c1">Text 3</div>
            </body>
        </html>
        """
        animator = Animator(document)
        divs = animator.find(class_='c1')

        divs[0].text = 'UPDATED'

        result = """
        <html>
            <body>
                <div class="c1">UPDATED</div>
                <div class="c2">Text 2</div>
                <div class="c1">Text 3</div>
            </body>
        </html>
        """.strip()
        self.assertEquals(result, animator.tostring())

import inelegant.finder

load_tests = inelegant.finder.TestFinder(__name__).load_tests

if __name__ == "__main__":
    unittest.main()
