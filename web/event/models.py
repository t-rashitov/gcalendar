from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    """
    Модель события
    """

    event_id = models.CharField('ID', max_length=100)
    event_type = models.CharField('Тип события', max_length=100)
    summary = models.CharField('Текст', max_length=2000, blank=True)
    start = models.DateTimeField('Дата начала события')
    end = models.DateTimeField('Дата окончания события')
    html_link = models.URLField('URL события')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f'{self.event_id} - {self.summary[:30]} с: {self.start} до: {self.end}'

    @classmethod
    def synchronize_with_remote(cls, events: list[dict], user: User) -> None:
        """
        Создает события из списка параметров, если события с такими event_id не существуют
        :param events: список параметров событий
        :param user: автор события
        :return:
        """

        current_events_ids = [event['event_id'] for event in events]
        Event.objects.filter(author=user).exclude(event_id__in=current_events_ids).delete()
        existing_events_ids = Event.objects.filter(author=user).values_list('event_id', flat=True)
        new_events = [
            Event(**params, author=user) for params in events if params['event_id'] not in existing_events_ids]

        if new_events:
            Event.objects.bulk_create(new_events)
