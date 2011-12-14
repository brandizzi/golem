from distutils.core import setup

setup(name='golem',
      version='0.1.1dev',
      description='Golem Unobtrusive Template',
      long_description="""
      Golem is an experimental, simple template engine for template animation
      (or unobtrusive server scripting). Golem allows developers to gelerate
      HTML interface for data based simple HTML mockups. Golem templates
      has no new tempalte syntax, no special XML elements, just plain HTML.
      """,
      author='Adam Victor Nazareth Brandizzi',
      author_email='brandizzi@gmail.com',
      url = 'http://bitbucket.org/brandizzi/golem',
      py_modules=['golem'],
      requires=['lxml (>=2.3)'],
     )
