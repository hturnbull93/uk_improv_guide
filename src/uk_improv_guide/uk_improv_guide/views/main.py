import datetime
from typing import Sequence

from pytz import timezone

from uk_improv_guide.models.event import Event, get_events_after_datetime

from django.shortcuts import render


def main(request):
    now:datetime.datetime = datetime.datetime.now(tz=timezone("Europe/London"))
    events:Sequence[Event] = get_events_after_datetime(now)
    return render(request, "main.html", {"title":"Events", "events":events})


