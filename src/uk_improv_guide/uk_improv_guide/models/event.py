import datetime
from typing import Sequence

import reversion
from django.db import models
from uk_improv_guide.lib.adminable import AdminableObject
from uk_improv_guide.lib.site_mappable import sitemap_model_object
from uk_improv_guide.lib.sitemaps import register_model_for_site_map
from uk_improv_guide.models.event_series import EventSeries
from uk_improv_guide.models.fields.fields import EVENTBRITE_LINK, FACEBOOK_LINK
from uk_improv_guide.models.team import Team
from uk_improv_guide.models.venue import Venue


@reversion.register
@register_model_for_site_map
class Event(sitemap_model_object("event"), AdminableObject, models.Model):
    EVENT_TYPES = (("S", "Show"), ("J", "Jam"), ("W", "Workshop"), ("A", "Audition"))
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="event/", blank=True)
    event_type = models.CharField(max_length=1, choices=EVENT_TYPES)
    start_time = models.DateTimeField(verbose_name="Show start time")
    facebook_link = FACEBOOK_LINK
    eventbrite_link = EVENTBRITE_LINK
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    series = models.ForeignKey(
        EventSeries, on_delete=models.SET_NULL, blank=True, null=True
    )
    teams = models.ManyToManyField(Team, verbose_name="teams playing", blank=True)

    def __str__(self):
        return f"{self.name} - @ {self.start_time} - {self.venue.name}"


def get_events_after_datetime(dt: datetime.datetime) -> Sequence[Event]:
    return Event.objects.filter(start_time__gte=dt).order_by("start_time")


def get_all_events() -> Sequence[Event]:
    return Event.objects.all()


def get_events_after_datetime_for_performer_id(
    dt: datetime.datetime, performer_id: int
) -> Sequence[Event]:
    return Event.objects.filter(
        start_time__gte=dt, teams__players__id=performer_id
    ).order_by("start_time")


def get_event_by_id(id: int) -> Event:
    e: Event = Event.objects.get(id=id)
    return e
