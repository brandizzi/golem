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

    def test_fill_list(self):
        template = """
            <html>
                <head><title>Some title stuff</title></head>
                <body>
                    <p>This is my wishlist:</p>
                    <ul class="wishlist">
                         <li>One item</li>
                         <li>Another item</li>
                    </ul>
                </body>
            </html>
        """

        wishlist = ['A poney', 'The Devil to Pay in the Backlands']
        
        animator = Animator(template)
        animator.fill('title', 'My wishlist')
        animator.fill('.wishlist li', wishlist)
        result = animator.result()

        parsed_result = fromstring(result)
        title = parsed_result.xpath('//title')[0]
        self.assertEquals(title.text, 'My wishlist')
        items = parsed_result.xpath('//li')
        self.assertItemsEqual([item.text for item in items], wishlist)

    def test_fill_href(self):
        template = """
            <html>
                <head><title>Golem</title></head>
                <body>
                    <p>Golem can be download from <a href="">here</a>.</p>
                </body>
            </html>
        """
        download_url = 'https://bitbucket.org/brandizzi/golem/downloads'

        animator = Animator(template)
        animator.fill('a', href=download_url)
        result = animator.result()

        parsed_result = fromstring(result)
        link = parsed_result.xpath('//a')[0]
        self.assertEquals(link.get('href'), download_url) 


if __name__ == "__main__":
    unittest.main()
