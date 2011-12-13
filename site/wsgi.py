import os.path

import cherrypy

import golem

site_dir = os.path.split(os.path.realpath(__file__))[0]
template_dir = os.path.join(site_dir, 'templates')
index_template_path = os.path.join(template_dir, 'index.html')
index_template = open(index_template_path).read()

class GolemSite(object):
    def index(self):
        animator = golem.Animator(index_template)

        animator.fill('a#downladPage', 
                href='https://bitbucket.org/brandizzi/golem/downloads')
        animator.fill('#version', '0.1.0')

        doctest_file = open(os.path.join(site_dir, os.path.pardir, 'golem.txt'))
        doctest = doctest_file.read()
        animator.fill("code.doctest", doctest)
        
        return animator.result()
    index.exposed = True

config = {'/': {}}
application =  cherrypy.tree.mount(GolemSite(), '', config=config)

if __name__ == "__main__":
    cherrypy.quickstart(GolemSite())
