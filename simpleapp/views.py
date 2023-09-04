from django.http import HttpResponse

from config import config


def index(request):
    simple_body = f"""
    <p>Hello, world. You're at the index page</p>
    <p>Some data from config are here:</p>
    <p>DAYS={config.FirstExample.DAYS}</p>
    <p>FIRST_DAY_OF_WEEK={config.FirstExample.FIRST_DAY_OF_WEEK}</p>
    <p>FUEL_PRICES={config.FirstExample.FUEL_PRICES}</p>
    <p>USE_CALENDAR={config.FirstExample.USE_CALENDAR}</p>
    <p>SECRET_SWITCH={config.FirstExample.SECRET_SWITCH}</p>
    <p>CONSOLIDATION_GROUPS={config.FirstExample.CONSOLIDATION_GROUPS}</p>

    <p>
    You can change configs <a href="/admin/liveconfigs/configrow/">here</a> and reload this page for checking changes.
    </p>
    """
    return HttpResponse(simple_body)
