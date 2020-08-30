# Princeton SEAS Faculty Scraper

This is a web scraper that produces machine-processable JSON and CSV feeds
of Princeton University's School of Engineering and Applied Science (SEAS)
faculty, sourced from [the official, publicly available faculty directory](https://engineering.princeton.edu/faculty-directory).

You can see [the JSON feed by clicking here](https://jlumbroso.github.io/princeton-scraper-seas-faculty/feeds/).

This feed is updated every week on Saturday. Read on to learn more.

## Accessing the static feeds

You can access the (regularly updated) JSON feed directly from this URL:
```text
https://jlumbroso.github.io/princeton-scraper-seas-faculty/feeds/
```
and the CSV feed is accessible from this URL:
```
https://jlumbroso.github.io/princeton-scraper-seas-faculty/feeds/index.csv
```

For example using Python, you can use the `requests` package to
get the JSON feed:
```python
import requests
r = requests.get("https://jlumbroso.github.io/princeton-scraper-seas-faculty/feeds/")
if r.ok:
    data = r.json()["data"]
```
You can use the [`comma`](https://github.com/jlumbroso/comma/) package to
get the CSV feed:
```python
import comma
data = comma.load(
    "https://jlumbroso.github.io/princeton-scraper-seas-faculty/feeds/index.csv",
    force_header=True)
```

## Feed format

This feed provides each person in the directory as a JSON dictionary with
the following fields:

```json
    {
      "netid": "lumbroso",
      "email": "lumbroso@cs.princeton.edu",
      "name": "J\u00e9r\u00e9mie Lumbroso",
      "first": "J\u00e9r\u00e9mie",
      "last": "Lumbroso",
      "profile-url": "https://engineering.princeton.edu/faculty/j-r-mie-lumbroso",
      "image": "https://engineering.princeton.edu/sites/default/files/thumbnails/image/Lumbroso_450x600_0.jpg",
      "website": "https://www.cs.princeton.edu/people/profile/lumbroso",
      "office": "035 Corwin Hall",
      "phone": "609-258-5379",
      "research": "Expertise: Probabilistic algorithms, data streaming, data structures, analysis of algorithms, analytic combinatorics.",
      "rank": "Lecturer",
      "affiliations": [
        "Computer Science"
      ]
    }
```

The CSV file follows this format (note that it does not contain the "research" field from the JSON format):

```csv
netid,email,name,first,last,profile-url,image,website,office,phone,rank,affiliations
lumbroso,lumbroso@cs.princeton.edu,Jérémie Lumbroso,Jérémie,Lumbroso,https://engineering.princeton.edu/faculty/j-r-mie-lumbroso,https://engineering.princeton.edu/sites/default/files/thumbnails/image/Lumbroso_450x600.jpg,https://www.cs.princeton.edu/people/profile/lumbroso,035 Corwin Hall,609-258-5379,Lecturer,Computer Science
```

## Acknowledgement & Backstory

This project was put together in August 2020, in preparation of the BSE freshpeople
advising period, co-organized with [Peter Bogucki and Traci Miller](https://engineering.princeton.edu/engage/leadership-and-staff).

I had often felt the need to have a programmatically accessible version of the faculty
directory, and made several (failed) attempts to address this need decisively. Often
my approach was too ambitious, for instance trying to aggregate the information of all
faculty on campus—despite the fact that this information is housed across many different
websites, which follow different formats and break at different intervals.

This time around, I decided to write a more focused project to robustly address this
need at least for SEAS faculty. This allowed me to integrate the faculty photos easily
within a project meant to make navigation for incoming students easier.

## License

This repository is licensed under [_The Unlicense_](LICENSE). This means I have no liability, but
you can do absolutely what you want with this.