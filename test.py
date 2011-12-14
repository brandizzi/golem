import cStringIO as StringIO

import unittest2 as unittest
from lxml.etree import fromstring, tostring

from golem import Animator, Filler

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

    def test_fillers_with_objects(self):
        template = """
            <html>
                <head><title>Golem</title></head>
                <body>
                    <table id="people">
                        <tr><th>Name</th><th>Age</th><th>Nick</th></tr>
                        <tr>
                            <td class="name">Foo</td>
                            <td class="age">1</td>
                            <td><input name="nick" type="text" /></td>
                        </tr>
                        <tr>
                            <td class="name">Bar</td>
                            <td class="age">2</td>
                            <td><input name="nick" type="text" /></td>
                        </tr>
                    </table>
                </body>
            </html>
        """
        download_url = 'https://bitbucket.org/brandizzi/golem/downloads'

        name_filler = Filler('td.name', lambda obj: obj.name)
        age_filler = Filler('td.age', lambda obj: obj.age)
        nick_filler = Filler('input[name="nick"]', value=lambda obj: obj.nick)

        class Person(object):
            def __init__(self, name, age, nick):
                self.name = name
                self.age = age
                self.nick = nick
        objects = [
            Person("John Smith", 42, 'Johny'),
            Person("Linda Carlson", 32, 'Linda'),
            Person("Ashley Johnson", 50, 'Ash')
        ]
        
        animator = Animator(template)
        fillers = [name_filler, age_filler, nick_filler]
        animator.fillSubelements('table#people', objects, fillers)
        result = animator.result()
        parsed_result = fromstring(result)
        name_tds = parsed_result.xpath('//td[@class="name"]')
        age_tds = parsed_result.xpath('//td[@class="age"]')
        nick_inputs = parsed_result.xpath('//input[@name="nick"]')
        paired = zip(objects, name_tds, age_tds, nick_inputs)
        for person, name_td, age_td, nick_input in paired:
            self.assertEquals(name_td.text, person.name)
            self.assertEquals(age_td.text, str(person.age))
            self.assertEquals(nick_input.get('value'), person.nick) 


if __name__ == "__main__":
    unittest.main()
