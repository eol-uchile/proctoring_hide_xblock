import json
import re
import pkg_resources

from django.template import Context, Template

from webob import Response

from xblock.core import XBlock
from xblock.fields import Integer, String, Boolean, Scope
from xblock.fragment import Fragment
from xblock.exceptions import JsonHandlerError
from xblock.completable import XBlockCompletionMode

# Make '_' a no-op so we can scrape strings
_ = lambda text: text


class ProctoringHideXBlock(XBlock):

    completion_mode = XBlockCompletionMode.EXCLUDED

    display_name = String(
        display_name=_("Display Name"),
        help=_("Display name for this module"),
        default="Proctoring Hide",
        scope=Scope.settings,
    )

    has_author_view = True

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        context_html = self.get_context()
        template = self.render_template('static/html/proctoring_hide.html', context_html)
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/proctoring_hide.css"))
        frag.add_javascript(self.resource_string("static/js/src/proctoring_hide.js"))
        settings = {
            'location': self.location
        }
        frag.initialize_js('ProctoringHideXBlock', json_args=settings)
        return frag

    def studio_view(self, context=None):
        context_html = self.get_context()
        template = self.render_template('static/html/studio.html', context_html)
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/proctoring_hide.css"))
        frag.add_javascript(self.resource_string("static/js/src/studio.js"))
        frag.initialize_js('ProctoringHideXBlock')
        return frag
    
    def author_view(self, context=None):
        context_html = self.get_context()
        template = self.render_template('static/html/author_view.html', context_html)
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/proctoring_hide.css"))
        return frag

    @XBlock.handler
    def studio_submit(self, request, suffix=''):
        self.display_name = request.params['display_name']
        return Response({'result': 'success'}, content_type='application/json')

    def get_context(self):
        return {
            'xblock': self
        }

    def render_template(self, template_path, context):
        template_str = self.resource_string(template_path)
        template = Template(template_str)
        return template.render(Context(context))

    @XBlock.json_handler
    def publish_completion(self, data, dispatch):  # pylint: disable=unused-argument
        """
        Entry point for completion for student_view.
        Parameters:
            data: JSON dict:
                key: "completion"
                value: float in range [0.0, 1.0]
            dispatch: Ignored.
        Return value: JSON response (200 on success, 400 for malformed data)
        """
        completion_service = self.runtime.service(self, 'completion')
        if completion_service is None:
            raise JsonHandlerError(500, u"No completion service found")
        elif not completion_service.completion_tracking_enabled():
            raise JsonHandlerError(404, u"Completion tracking is not enabled and API calls are unexpected")
        if not isinstance(data['completion'], (int, float)):
            message = u"Invalid completion value {}. Must be a float in range [0.0, 1.0]"
            raise JsonHandlerError(400, message.format(data['completion']))
        elif not 0.0 <= data['completion'] <= 1.0:
            message = u"Invalid completion value {}. Must be in range [0.0, 1.0]"
            raise JsonHandlerError(400, message.format(data['completion']))
        self.runtime.publish(self, "completion", data)
        return {"result": "ok"}



    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ProctoringHideXBlock",
             """<proctoring_hide/>
             """),
        ]
