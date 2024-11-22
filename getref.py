#!/usr/bin/env python3
#
# Script for formatting a reference in BibTeX format, from a DOI.
#

import argparse
import requests
import sys

from db import Article


def parse_args():
    parser = argparse.ArgumentParser('Get BibTeX reference from DOI')

    parser.add_argument('doi', help="DOI or URL to extract BibTeX reference from.")

    return parser.parse_args()


def formatBibTeX(article):
    """
    Format a BibTeX reference, given a DOI JSON object.
    """
    authors = article.authors.split(', ')
    refname = authors[0].split(' ')[-1] + article.date[:4]
    for i in range(len(authors)):
        if '.' not in authors[i]:
            authors[i] = '{' + authors[i] + '}'

    authorlist = ' and '.join(authors)

    s  =f"@article {{{refname},\n"
    s +=f"    title = {{{article.title}}},\n"
    s +=f"    author = {{{authorlist}}},\n"
    s +=f"    journal = {{{article.journal}}},\n"
    s +=f"    volume = {{{article.volume}}},\n"
    s +=f"    pages = {{{article.pages}}},\n"
    s +=f"    issue = {{{article.issue}}},\n"
    s +=f"    year = {{{article.date[:4]}}},\n"
    s +=f"    doi = {{{article.doi}}},\n"
    s +=f"    url = {{{article.url}}}\n"
    s += "}"

    return s


def main():
    args = parse_args()

    art = Article.fromDOI(args.doi)
    print(formatBibTeX(art))

    return 0


if __name__ == '__main__':
    sys.exit(main())


