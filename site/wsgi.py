import os.path
import sqlite3

import cherrypy

import golem

from comment import Comment, get_all_comments, create_comment_table, save_comment

site_dir = os.path.split(os.path.realpath(__file__))[0]
template_dir = os.path.join(site_dir, 'templates')
index_template_path = os.path.join(template_dir, 'index.html')
index_template = open(index_template_path).read()

db_dir = os.path.join(site_dir, 'golemsite.db')

connection = sqlite3.connect(db_dir)
create_comment_table(connection)
connection.close()

class GolemSite(object):
    def index(self):
        connection = sqlite3.connect(db_dir, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        animator = golem.Animator(index_template)

        animator.fill('a#downladPage', 
                href='https://bitbucket.org/brandizzi/golem/downloads')
        animator.fill('#version', '0.1.0')

        doctest_file = open(os.path.join(site_dir, os.path.pardir, 'golem.txt'))
        doctest = doctest_file.read()
        animator.fill("code.doctest", doctest)

        comments = get_all_comments(connection)
        fillers = [
                golem.Filler('.author .name', lambda c: c.author),
                golem.Filler('.author .date', lambda c: c.date.isoformat()),
                golem.Filler('.author a', 
                        lambda c: c.author_url, href=lambda c: c.author_url),
                golem.Filler('.title', lambda c: c.title),
                golem.Filler('.content', lambda c: c.content),
        ]
        animator.fillSubelements('#comments', comments, fillers)
        connection.close()
        return animator.result()
    index.exposed = True

    def comment(self, author, author_url, title, content):
        comment = Comment(author, author_url, title, content)
        connection = sqlite3.connect(db_dir, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        save_comment(connection, comment)
        connection.close()
        raise cherrypy.HTTPRedirect('/')
    comment.exposed = True

config = {'/': {}}
application =  cherrypy.tree.mount(GolemSite(), '', config=config)

if __name__ == "__main__":
    cherrypy.quickstart(GolemSite())
