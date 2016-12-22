"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from reference.models import Reference
loader = ResourceLoader(__name__)
from django.utils.translation import ugettext_lazy, ugettext


class DummyXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # TO-DO: delete count, and define your own fields.
    # ref_list = String(
    #     default='',
    #     scope=Scope.settings,
    #     help=ugettext_lazy("References ids container.")
    # )
    ref_list = List(
        default=[],
        scope=Scope.settings,
        help=ugettext_lazy("References ids container.")
    )

    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the DummyXBlock, shown to students
        when viewing courses.
        """
        # html = self.resource_string("static/html/dummyblock.html")
        # frag = Fragment(html.format(self=self))
        references = Reference.alive_references(ids=self.ref_list)

        frag = Fragment()
        frag.add_content(
            loader.render_template('static/html/dummyblock.html',
                                    {'references': references, 'self': self}
                                )
            )
        frag.add_css(self.resource_string("static/css/dummyblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/dummyblock.js"))
        frag.initialize_js('DummyXBlock')
        return frag

    # TO-DO: change this view to display your data your own way.
    def studio_view(self, context=None):
        """This is the view displaying xblock form in studio.
         to get course key: self.parent.course_key._to_string()
         to get user id : self.runtime._user.id
         """
        # import pdb
        # pdb.set_trace()

        references = Reference.alive_references(ids=None)
        frag = Fragment()
        frag.add_content(
            loader.render_template('static/html/dummy_block_studio.html',
                                    {'references': references, 'self': self}
                                )
            )
        frag.add_css(self.resource_string('static/css/studio.css'))
        frag.add_javascript(
            self.resource_string("static/js/src/dummyBlockStudio.js"))
        frag.initialize_js('DummyXBlockStudio')
        return frag

    @XBlock.json_handler
    def add_reference_to_course(self, data, suffix=''):

        # refrence_list = repr(self.ref_list)
        refrence_list = self.ref_list

        reference = int(data.get('reference'))
        requested_action = data.get('requested_action')

        if requested_action not in ['add', 'remove']:
            return {'status' : 400, 'message' : 'Invalid requeset.'}

        if requested_action == 'add':
            if reference in refrence_list:
                return {'status' : 304, 'message' : 'Allready added.'}

            refrence_list.append(reference)
            response = {'status' : 200, 'message' : 'Added.'}


        if requested_action == 'remove':
            if reference not in refrence_list:
                return {'status' : 404, 'message' : 'Not found.'}

            refrence_list.remove(reference)
            response = {'status' : 200, 'message' : 'Removed.'}

        # self.ref_list = repr(refrence_list)
        self.ref_list = refrence_list

        return response

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("DummyXBlock",
             """<dummyblock/>
             """),
            ("Multiple DummyXBlock",
             """<vertical_demo>
                <dummyblock/>
                <dummyblock/>
                <dummyblock/>
                </vertical_demo>
             """),
        ]
