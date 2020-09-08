
import typing
import urllib.parse

import requests
import bs4

import princeton_scraper_seas_faculty.campus_directory
import princeton_scraper_seas_faculty.constants
import princeton_scraper_seas_faculty.helpers


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "SeasFacultyInformation",
    "fetch_seas_faculty_directory",
]


# SEAS directory info type

SeasFacultyInformation = typing.TypedDict(
    "SeasFacultyInformation", {
        "netid": str,
        "email": str,
        "name": str,
        "first": str,
        "last": str,
        "profile-url": str,
        "image": str,
        "website": str,
        "office": str,
        "phone": str,
        "research": str,
        "rank": str,
        "affiliations": typing.List[str],
    }, total=False)


#  URL to retrieve the SEAS directory

PRINCETON_SEAS_DIRECTORY_BASE = "https://engineering.princeton.edu/"
PRINCETON_SEAS_DIRECTORY_URL = urllib.parse.urljoin(
    PRINCETON_SEAS_DIRECTORY_BASE,
    "/faculty-directory"
)


# Hard-coded constants that are required to scrape the web page

CLASS_ITEM = "directory-item"
CLASS_OFFICE = "office"
CLASS_PHONE = "phone"
CLASS_RESEARCH = "research-area"
CLASS_PRIMARY_AFF = "primary-affiliations"
CLASS_OTHER_AFF = "other-affiliations"

STR_EMAIL = "Email"
STR_WEBSITE = "Website"
STR_OFFICE = "Office:"
STR_PHONE = "Phone:"
STR_PRIMARY_AFF = "Primary Affiliations:"
STR_OTHER_AFF = "Other Affiliations:"
STR_RESEARCH = "Research Interests:"


def _from_tag_or_string_to_string(tag_or_string: typing.Union[str, bs4.element.Tag]) -> str:
    """
    Returns text, given either a string or a BeautifulSoup DOM subtree.

    :param tag_or_string: A BeautifulSoup `bs4.element.Tag` or `str`

    :return: The text content of that tag
    """
    if type(tag_or_string) is str:
        return tag_or_string
    if type(tag_or_string) is bs4.element.Tag:
        return tag_or_string.text

    # should not happen, but better than None as a default
    return str(tag_or_string)


def parse_affiliation_and_rank(tag_or_string: typing.Union[str, bs4.element.Tag]) -> SeasFacultyInformation:
    """
    Returns the rank and affiliation from the header of a SEAS directory item.

    :param tag_or_string: The DOM subtree for the directory item's caption (<H4></H4>),
    as a BeautifulSoup `bs4.element.Tag` or `str`

    :return: A dictionary with two fields, `"rank"` and `"affiliations"`
    """
    s = _from_tag_or_string_to_string(tag_or_string)

    # work variables
    likely_rank = ""
    likely_affiliations = []

    for rank_candidate in princeton_scraper_seas_faculty.constants.RANKS:
        if rank_candidate in s:
            # heuristic: If the candidate is longer than what we have
            # assume it will more accurately describe person
            if len(likely_rank) < len(rank_candidate):
                likely_rank = rank_candidate

    for affiliation in princeton_scraper_seas_faculty.constants.DEPARTMENTS:
        if affiliation in s:
            likely_affiliations.append(affiliation)

    return {
        "rank": likely_rank,
        "affiliations": likely_affiliations,
    }


def parse_directory_item(block: bs4.element.Tag, fast: bool = False) -> SeasFacultyInformation:
    """
    Returns a parsed `SeasFacultyInformation` dictionary, provided a DOM subtree
    of a block representing one item of the SEAS directory page.

    :param block: The DOM subtree for the directory item, as a BeautifulSoup `bs4.element.Tag`

    :param fast: Determines whether some optimizations should be made to avoid making
    many HTTP requests (but at the expense of data accuracy); unless speed is a
    consideration, set this to `False`.

    :return: The parsed directory item as a `SeasFacultyInformation` dictionary
    """

    dirinfo = {}

    # parse the email
    tag_email = block.find("a", string=STR_EMAIL)
    if tag_email is not None:
        email = tag_email["href"].replace("mailto:", "").strip()
        # noinspection PyBroadException
        try:
            netid = princeton_scraper_seas_faculty.campus_directory.find_netid_from_princeton_email(
                princeton_email=email, fast=fast)
        except:
            netid = None

        dirinfo["netid"] = netid
        dirinfo["email"] = email

    # parse the name
    tag_name = block.find("h3")
    if tag_name is not None:
        dirinfo["name"] = tag_name.text.strip()

        first, last = princeton_scraper_seas_faculty.helpers.split_name(dirinfo["name"])
        dirinfo["first"] = first
        dirinfo["last"] = last

    # parse the profile URL
    tag_profile_url = tag_name.find("a")
    if tag_profile_url is not None:
        dirinfo["profile-url"] = urllib.parse.urljoin(
            PRINCETON_SEAS_DIRECTORY_BASE,
            tag_profile_url["href"])

    # parse the image
    tag_img = block.find("img")
    if tag_img is not None:
        dirinfo["image-url"] = tag_img.get("src", "")

    # parse the web address
    tag_email = block.find("a", string=STR_WEBSITE)
    if tag_email is not None:
        dirinfo["website"] = tag_email["href"]

    # parse the office
    tag_office = block.find("p", attrs={"class": CLASS_OFFICE})
    if tag_office is not None:

        # compute and clean up the string
        s_office = tag_office.text
        s_office = s_office.replace(STR_OFFICE, "")
        s_office = s_office.strip()

        dirinfo["office"] = s_office

    # parse the phone number
    tag_phone = block.find("p", attrs={"class": CLASS_PHONE})
    if tag_phone is not None:

        # compute and clean up the string
        s_phone = tag_phone.text
        s_phone = s_phone.replace(STR_PHONE, "")
        s_phone = s_phone.strip()

        dirinfo["phone"] = s_phone

    # parse the research interests
    tag_research = block.find("p", attrs={"class": CLASS_RESEARCH})
    if tag_research is not None:

        # compute and clean up the string
        s_research = tag_research.text
        s_research = s_research.replace(STR_RESEARCH, "")
        s_research = s_research.strip()

        dirinfo["research"] = s_research

    ############################################################

    # parse affiliation (old version)
    #tag_affiliation = block.find("p", attrs={"class": CLASS_PRIMARY_AFF})
    #if tag_affiliation is not None:
    #
    #    # compute and clean up the string
    #    s_affiliation = tag_affiliation.text
    #    s_affiliation = s_affiliation.replace(STR_PRIMARY_AFF, "")
    #    s_affiliation = s_affiliation.strip()
    #
    #    dirinfo["affiliation"] = s_affiliation

    # parse affiliation and rank
    tag_bigstring = block.find("h4")
    if tag_bigstring is not None:
        data = parse_affiliation_and_rank(tag_bigstring)
        dirinfo.update(data)

    return dirinfo


def fetch_seas_faculty_directory(fast: bool = False) -> typing.Optional[typing.List[SeasFacultyInformation]]:
    """
    Retrieves and parses a copy of the Princeton SEAS faculty directory, as
    hosted at: `https://engineering.princeton.edu/faculty-directory`.

    :param fast: Determines whether some optimizations should be made to avoid making
    many HTTP requests (but at the expense of data accuracy); unless speed is a
    consideration, set this to `False`.

    :return: A list of `SeasFacultyInformation` dictionaries containing the public
    faculty directory information
    """

    r = requests.get(PRINCETON_SEAS_DIRECTORY_URL)
    if not r.ok:
        return

    s = bs4.BeautifulSoup(r.content, features="html.parser")
    if s is None:
        return

    directory_items = s.find_all("div", attrs={"class": CLASS_ITEM})

    directory_data = list(map(
        lambda t: parse_directory_item(t, fast=fast),
        directory_items))

    return directory_data


