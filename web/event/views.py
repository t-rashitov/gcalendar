import logging

from django.shortcuts import redirect
from django.views.generic import TemplateView

from event.exceptions import LoadError, AuthError
from event.models import Event
from event.services import GoogleEventsService

logger = logging.getLogger('django')


class EventListView(TemplateView):
    template_name = 'events-list.html'
    service_class = GoogleEventsService

    def get_service(self):
        return self.service_class.get_service(user=self.request.user)

    def get(self, request, *args, **kwargs):

        context = {}

        try:
            service = self.get_service()  # type: GoogleEventsService
            service.synchronize_with_remote()

        except AuthError as e:
            logger.info(str(e))
            return redirect('logout')
        except LoadError as e:
            logger.warning(str(e))
            context.update({'errors': ['Не удалось синхронизировать события.']})

        context.update({'events': Event.objects.filter(author=request.user).order_by('-start')[:1000]})

        return self.render_to_response(context)
