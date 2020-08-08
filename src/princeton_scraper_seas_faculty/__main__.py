
import datetime
import json
import sys


# noinspection PyBroadException
if __name__ == "__main__":
    try:
        from princeton_scraper_seas_faculty.seas_faculty_directory import fetch_seas_faculty_directory
        data = fetch_seas_faculty_directory(fast=True)
        print(json.dumps({
            "source": "https://github.com/jlumbroso/princeton-scraper-seas-faculty/",
            "timestamp": datetime.datetime.now().isoformat(),
            "data": data,
        }, indent=2))
        sys.exit(0)
    except Exception:
        sys.exit(1)
