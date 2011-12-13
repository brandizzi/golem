import cStringIO as StringIO

import unittest2 as unittest
from lxml.etree import fromstring

from golem import Animator

class SimpleAnimationTestCase(unittest.TestCase):

    def test_fill_title_span(self):
        template = """
            <html>
                <head><title>This is my title</title></head>
                <body>
                    <p>
                        This is
                        <span id="message">my message to the world</span>
                    </p>
                </body>
            </html>
        """
        animator = Animator(template)
        animator.fill('title', 'Message title')
        animator.fill('#message', 'my lovely message')
        result = animator.result()

        parsed_result = fromstring(result)
        title = parsed_result.xpath('//title')[0]
        self.assertEquals(title.text, 'Message title')
        span = parsed_result.xpath('//span')[0]
        self.assertEquals(span.text, 'my lovely message')


if __name__ == "__main__":
    unittest.main()
