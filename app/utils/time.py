import pytz
from datetime import datetime

utc = pytz.timezone("UTC")

def localize(dt: datetime)->datetime:
    return utc.localize(dt).astimezone(pytz.timezone("America/New_York"))