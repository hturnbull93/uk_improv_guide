import logging
from typing import Sequence

from django.shortcuts import render
from uk_improv_guide.models import Event, Team
from uk_improv_guide.models.performer import Performer, get_performer_by_id

log = logging.getLogger(__name__)


def performer(request, id: int):
    this_performer: Performer = get_performer_by_id(id)

    teams: Sequence[Team] = this_performer.plays_for.all

    events: Sequence[Event] = Event.objects.all()

    return render(
        request,
        "performer.html",
        {
            "title": f"{this_performer.full_name()}",
            "performer": this_performer,
            "teams": teams,
            "events": events,
        },
    )
