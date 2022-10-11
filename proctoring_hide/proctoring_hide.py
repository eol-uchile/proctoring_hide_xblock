import json
import re
import pkg_resources

from django.template import Context, Template

from webob import Response
from django.conf import settings as DJANGO_SETTINGS
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

    def show_staff_grading_interface(self):
        """
        Return if current user is staff and not in studio.
        """
        in_studio_preview = self.scope_ids.user_id is None
        return self.is_course_staff() and not in_studio_preview

    def is_course_staff(self):
        # pylint: disable=no-member
        """
         Check if user is course staff.
        """
        return getattr(self.xmodule_runtime, 'user_is_staff', False)

    def student_view(self, context=None):
        template = self.render_template('static/html/proctoring_hide.html', {'is_staff': self.show_staff_grading_interface()})
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/proctoring_hide.css"))
        frag.add_javascript(self.resource_string("static/js/src/proctoring_hide.js"))
        settings = {
            'proctor_url': DJANGO_SETTINGS.PROCTORING_HIDE_URL,
            'is_staff': self.show_staff_grading_interface()
        }

        frag.initialize_js('ProctoringHideXBlock', json_args=settings)
        return frag

    def studio_view(self, context=None):
        template = self.render_template('static/html/studio.html', {})
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/proctoring_hide.css"))
        frag.add_javascript(self.resource_string("static/js/src/studio.js"))
        frag.initialize_js('ProctoringHideXBlock')
        return frag
    
    def author_view(self, context=None):
        template = self.render_template('static/html/author_view.html', {})
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/proctoring_hide.css"))
        return frag

    @XBlock.handler
    def studio_submit(self, request, suffix=''):
        self.display_name = request.params['display_name']
        return Response({'result': 'success'}, content_type='application/json')

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
