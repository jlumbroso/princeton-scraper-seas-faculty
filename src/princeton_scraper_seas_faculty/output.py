
import comma
import datetime
import json

import princeton_scraper_seas_faculty.seas_faculty_directory


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "json_output",
    "csv_output",
]


# noinspection PyBroadException
def json_output(fast: bool = False):
    try:
        data = princeton_scraper_seas_faculty.seas_faculty_directory.fetch_seas_faculty_directory(fast=fast)
        return json.dumps({
            "source": "https://github.com/jlumbroso/princeton-scraper-seas-faculty/",
            "timestamp": datetime.datetime.now().isoformat(),
            "data": data,
        }, indent=2)
    except Exception:
        return


def csv_output(fast: bool = False):
    try:
        data = princeton_scraper_seas_faculty.seas_faculty_directory.fetch_seas_faculty_directory(fast=fast)
        for row in data:
            del row["research"]
            row["affiliations"] = ";".join(row["affiliations"])
        return comma.dumps(data)
    except Exception:
        return
