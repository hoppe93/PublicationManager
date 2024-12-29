
import feedparser
import requests


def fromArXiv(arxiv_id):
    """
    Fetch article details from its arXiv ID (or URL).
    """
    if 'arxiv.org' in arxiv_id:
        idx = arxiv_id.rfind('/')+1
        arxiv_id = arxiv_id[idx:]

    r = requests.get(f'https://export.arxiv.org/api/query?id_list={arxiv_id}')

    if r.status_code == 200:
        feed = feedparser.parse(r.text)
        return feed.entries[0]
    else:
        raise Exception(f"Error when fetching arXiv. The server returned HTTP status code '{r.status_code}: {r.reason}'.")


def fromDOI(doi):
    """
    Fetch article details from its DOI number (or URL).
    """
    if doi[8:] == 'https://':
        idx = doi[8:].find('/')+8+1
        doi = doi[idx:]

    r = requests.get(
        f'https://doi.org/{doi}',
        headers={
            'Accept': 'application/vnd.citationstyles.csl+json',
            'q': '1.0'
        }
    )

    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Error when fetching DOI. The server returned HTTP status code '{r.status_code}: {r.reason}'.")


