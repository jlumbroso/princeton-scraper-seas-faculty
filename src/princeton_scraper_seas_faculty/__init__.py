
"""
Library to fetch and parse the public Princeton SEAS Faculty directory as a
Python dictionary or JSON data source.
"""

__version__ = '1.0.0'

__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
]


from princeton_scraper_seas_faculty.seas_faculty_directory import SeasFacultyInformation
from princeton_scraper_seas_faculty.seas_faculty_directory import fetch_seas_faculty_directory


version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split('.'))

