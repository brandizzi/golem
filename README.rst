=====
Golem
=====

Golem is an experimental, simple template engine for template animation
(or unobtrusive server scripting). Golem allows developers to gelerate
HTML interface for data based simple HTML mockups. Golem templates
has no new template syntax, no special XML elements, just plain HTML.

I wrote it for fun, inspired by  `this post`_ and `this Stack Overflow
question`_.

.. _`this post`: http://www.workingsoftware.com.au/page/Your_templating_engine_sucks_and_everything_you_have_ever_written_is_spaghetti_code_yes_you

.. _`this Stack Overflow question`: http://stackoverflow.com/questions/8478943/

How to use it?
==============

Just write a mockup with pure HTML::

    >>> my_html = """<html>
    ...     <head><title>I will think about a title some day</title></head>
    ...     <body>
    ...         <p>My wishlist</p>
    ...         <ul class="wishlist">
    ...             <li>Some wish here</li>
    ...             <li>Some wish here</li>
    ...         </ul>
    ...         <p>You can buy this stuff at 
    ...         <a id="shop" href="">this shop</a></p>
    ...     </body>
    ... </html>"""

Now Python should do the rest! First create an Animator::

    >>> import golem
    >>> animator = golem.Animator(my_html)

Then inform animator about the data to fill the mock-up. For example, to set a
meaningful title, call the fill() method with a CSS selector for the 
<title> tag and the value to be put there::

    >>> animator.fill('title', 'My wishlist')

To set the items in the wishlist, give the method a selector to the <li>
elements but pass a list to it as a second parameter::

    >>> animator.fill('.wishlist li', 
    ...         ['A poney', 'candies', 'The Devil to Pay in the Backlands'])

To set the href attribute from the <a> element, pass the value to be set
as a named parameter::

    >>> animator.fill('a#shop', href='http://mymockshop.com')

The result() method presents the filled template::

    >>> print(animator.result())
    <html>
        <head><title>My wishlist</title></head>
        <body>
            <p>My wishlist</p>
            <ul class="wishlist">
                <li>A poney</li>
                <li>candies</li>
                <li>The Devil to Pay in the Backlands</li>
                </ul>
            <p>You can buy this stuff at 
            <a id="shop" href="http://mymockshop.com">this shop</a></p>
        </body>
    </html>
 
``Filler`` objects
==================

Those are too simple examples, however. How would Golem do stuff to complex
structures, like tables? Given the class below...

::

    >>> class Person(object):
    ...     def __init__(self, name, age, nickname):
    ...         self.name = name
    ...         self.age = age
    ...         self.nickname = nickname

...how would it deal, let us say, with the table below...

::

    >>> my_table = """<html>
    ...     <head><title>Golem</title></head>
    ...     <body>
    ...         <table id="people">
    ...         <tr><th>Name</th><th>Age</th><th>Nick</th></tr>
    ...                 <tr>
    ...                 <td class="name">Foo</td>
    ...                 <td class="age">1</td>
    ...                 <td><input name="nick" type="text" /></td>
    ...             </tr>
    ...             <tr>
    ...                 <td class="name">Bar</td>
    ...                 <td class="age">2</td>
    ...                 <td><input name="nick" type="text" /></td>
    ...             </tr>
    ...         </table>
    ...    </body>
    ... </html>"""

...if we have to populate it with the objects below?

::

    >>> people = [
    ...     Person("John Smith", 42, 'Johny'),
    ...     Person("Linda Carlson", 32, 'Linda'),
    ...     Person("Ashley Johnson", 50, 'Ash')
    ... ]

Well, we will use golem.Filler objects. A filler should know the selector
of the element it will fill, as well a function to fill the element. For
example, the name_filler below will fill a <td> (with the class 
name) with the name attribute of an object::

    >>> name_filler = golem.Filler('td.name', lambda obj: obj.name)

Same for the age::

    >>> age_filler = golem.Filler('td.age', lambda obj: obj.age)

The <input> is more complex since we should fill an attribute, not the text
of the element. However, it is no problem: just pass the attribute filler as
a named parameter. The name of the parameter should be the name of the
attribute::

    >>> nick_filler = golem.Filler(
    ...        'input[name="nick"]', value=lambda o: o.nickname)

Now, we create an animator for our new document::

    >>> animator = golem.Animator(my_table)

We should inform the animator which element contains all the subelements to
be filled - in this case, the outer element is the <table> with id 
"people". It is done by the fillSubelements() method, which receives
the selector of the outer element, the objects and the fillers::

    >>> animator.fillSubelements('table#people', people, 
    ...      [name_filler, age_filler, nick_filler])

That is it! Now, just call result()::

    >>> print(animator.result())
    <html>
        <head><title>Golem</title></head>
        <body>
            <table id="people">
            <tr><th>Name</th><th>Age</th><th>Nick</th></tr>
                    <tr>
                    <td class="name">John Smith</td>
                    <td class="age">42</td>
                    <td><input name="nick" type="text" value="Johny"/></td>
                </tr>
                <tr>
                    <td class="name">Linda Carlson</td>
                    <td class="age">32</td>
                    <td><input name="nick" type="text" value="Linda"/></td>
                </tr>
                <tr>
                    <td class="name">Ashley Johnson</td>
                    <td class="age">50</td>
                    <td><input name="nick" type="text" value="Ash"/></td>
                </tr>
                </table>
       </body>
    </html>
