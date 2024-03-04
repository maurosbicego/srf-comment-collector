from datetime import datetime

def parseDate(date: str) -> datetime:
    return datetime.strptime(date[:-6],"%Y-%m-%dT%H:%M:%S")