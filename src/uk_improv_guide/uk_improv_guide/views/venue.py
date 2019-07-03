import logging
import pprint
from typing import Sequence

from django.shortcuts import render
from uk_improv_guide.lib.opengraph import opengraph_website
from uk_improv_guide.models import Event
from uk_improv_guide.models.venue import Venue, get_venue_by_id

log = logging.getLogger(__name__)


def venue(request, id: int):
    this_venue: Venue = get_venue_by_id(id)
    title = this_venue.name

    log.info(pprint.pformat(dir(this_venue)))

    events: Sequence[Event] = this_venue.event_set.all()

    return render(
        request,
        "venue.html",
        {
            "title": title,
            "venue": this_venue,
            "events": events,
            "og": opengraph_website(
                title=title, url=request.build_absolute_uri(), image=this_venue.image
            ),
        },
    )
