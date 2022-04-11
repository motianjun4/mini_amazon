import pytz
from datetime import datetime

utc = pytz.timezone("UTC")

def localize(dt: datetime)->datetime:
    return utc.localize(dt).astimezone(pytz.timezone("America/New_York"))

def iso(dt: datetime)->str:
    return dt.isoformat()

def strtime(dt: datetime)->str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def strdate(dt: datetime)->str:
    return dt.strftime("%Y-%m-%d")

def get_now()->datetime:
    return datetime.now().astimezone(pytz.utc)