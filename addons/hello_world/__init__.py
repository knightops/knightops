# from flask import flash, Blueprint, render_template, render_template_string
# from flask_plugins import connect_event
# from example.app import AppPlugin
#
from core.addons import Addons
__plugin__ = "HelloWorld"
__version__ = "1.0.0"
#
#
# def hello_world():
#     flash("Hello World from {} Plugin".format(__plugin__), "success")
#
#
# def hello_world2():
#     flash("Hello World 2 from {} Plugin".format(__plugin__), "success")
#
#
# def inject_hello_world():
#     return "<h1>Hello World Injected</h1>"
#
#
# def inject_hello_world2():
#     return "<h1>Hello World 2 Injected</h1>"
#
#
# def inject_navigation_link():
#     return render_template_string(
#         """
#             <li><a href="{{ url_for('hello.index') }}">Hello</a></li>
#         """)
#
#
# hello = Blueprint("hello", __name__, template_folder="templates")
#
#
# @hello.route("/")
# def index():
#     return render_template("hello.html")
#
#
# class HelloWorld(AppPlugin):
class HelloWorld(Addons):

    def setup(self):
        pass
        # self.register_blueprint(hello, url_prefix="/hello")
        #
        # connect_event("after_navigation", hello_world)
        # connect_event("after_navigation", hello_world2)
        #
        # connect_event("tmpl_before_content", inject_hello_world)
        # connect_event("tmpl_before_content", inject_hello_world2)
        #
        # connect_event("tmpl_navigation_last", inject_navigation_link)

print('hello work')
