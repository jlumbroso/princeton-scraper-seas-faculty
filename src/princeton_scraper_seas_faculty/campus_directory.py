
import typing
import urllib.parse

import requests
import bs4


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "find_netid_from_princeton_email"
]


# URL to build queries to search the campus directory by email address equality
# NOTE: had to switch to "begins with" because of bug in search

# PRINCETON_CAMPUS_DIRECTORY_EMAIL_SEARCH_URL = "https://www.princeton.edu/search/people-advanced?e={}&ef=eq"
PRINCETON_CAMPUS_DIRECTORY_EMAIL_SEARCH_URL = "https://www.princeton.edu/search/people-advanced?e={}&ef=b"
PRINCETON_CAMPUS_DIRECTORY_NETID_SEARCH_URL = "https://www.princeton.edu/search/people-advanced?i={}&if=eq"

# Hard-coded constants that are required to scrape the web page

CLASS_RESULTS_BLOCK1 = "people-results"
CLASS_RESULTS_BLOCK2 = "bordered"
CLASS_RESULTS_ROW = "row"
CLASS_RESULTS_DETAILS = "expanded-details-value"

STR_NETID = "NetID"


# problem children! (emails that somehow do not show up in the campus directory)

MANUAL_NETID_FROM_PRINCETON_EMAIL = {
    "a_a_a@princeton.edu": "aaa"
}


def _is_likely_netid(s: str) -> bool:
    if type(s) is not str or len(s) == 0:
        return False

    # A NetID is a alphanumerical string no longer than
    # 8 characters
    return len(s) <= 8 and s.isalnum()


# noinspection PyBroadException
def fetch_campus_directory_results(url: str) -> typing.Optional[typing.List[bs4.element.Tag]]:
    """

    :param url:
    :return:
    """

    # not a valid URL
    if url is None or type(url) is not str or len(url) == 0 or "http" not in url:
        return

    # make request
    r = requests.get(url)
    if not r.ok:
        return

    # parse using BeautifulSoup
    s = bs4.BeautifulSoup(r.content, features="html.parser")
    if s is None:
        return

    # try to extract the subtree of results
    try:
        # get the subtree of the DOM containing results
        b = s.find("div", attrs={"class": CLASS_RESULTS_BLOCK1}).find("div", attrs={"class": CLASS_RESULTS_BLOCK2})

        # get individual results
        raw_items = b.find_all("div", attrs={"class": CLASS_RESULTS_ROW})

        # ensure there are least one
        if raw_items is None:
            return

    except:
        return

    return raw_items


def find_netid_from_princeton_email(princeton_email: str, fast: bool = False) -> typing.Optional[str]:
    """
    Returns the NetID of a campus member, given a valid Princeton email; this
    places a query with the central campus directory as available publicly from:
    `https://search.princeton.edu`.

    :param princeton_email: A valid email, using the `@princeton.edu` domain.
    :param fast: Determines whether to use a heuristic to avoid doing too many requests;
    unless speed is a requirement, should be set to `False`.
    :return: The NetID of the person whose email was provided as an argument.
    """

    # hack to deal with hits that somehow don't work
    princeton_email = princeton_email.lower()
    if princeton_email in MANUAL_NETID_FROM_PRINCETON_EMAIL:
        return MANUAL_NETID_FROM_PRINCETON_EMAIL[princeton_email]

    # this is a heuristic that can save a lot of lookups (but may not
    # work in some unfortunate cases)
    email_prefix = princeton_email.split("@")[0].lower()
    if fast:
        if _is_likely_netid(email_prefix):
            return email_prefix

    # NOTE: maybe this heuristic is too much?
    best_guess = email_prefix

    #url = PRINCETON_CAMPUS_DIRECTORY_EMAIL_SEARCH_URL.format(
    #    urllib.parse.quote(princeton_email))
    # NOTE: attempted fix to handle @cs.princeton.edu addresses better
    url = PRINCETON_CAMPUS_DIRECTORY_EMAIL_SEARCH_URL.format(
            email_prefix + urllib.parse.quote("@"))

    raw_items = fetch_campus_directory_results(url=url)

    if raw_items is None or len(raw_items) == 0:
        return best_guess

    if len(raw_items) > 1:
        raise Exception("should not have more than one result")

    first = raw_items[0]
    tag_netid_label = first.find("h4", string=STR_NETID)
    if tag_netid_label is None:
        return best_guess

    tag_netid = tag_netid_label.find_next_sibling("span", attrs={"class": CLASS_RESULTS_DETAILS})
    if tag_netid is None:
        return best_guess

    return tag_netid.text.strip().lower()



