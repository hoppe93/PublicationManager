# Helper class for formatting references

from db import Setting


ABBREVIATIONS = {
    'Computer Physics Communications': 'Comput. Phys. Commun.',
    'Nuclear Fusion': 'Nucl. Fusion',
    'Journal of Plasma Physics': 'J. Plasma Phys.',
    'Physics of Plasmas': 'Phys. Plasmas',
    'Physical Review Letters': 'Phys. Rev. Lett.',
    'Plasma Physics and Controlled Fusion': 'Plasma Phys. Contr. F',
}


def format(s, article, maxauthors=100, abbrjournal=False, includeperiods=False):
    """
    Format the given article using the given code string.
    """
    glbls = dict(
        doi=article.doi,
        title=article.title,
        url=article.url,
        pinboard=article.pinboard,
        volume=article.volume,
        issue=article.issue,
        pages=article.pages,
        date=article.date,
        year=article.date.year,
        retval=None
    )

    if maxauthors:
        authors = article.authors.split(', ')
        glbls['nauthors'] = len(authors)
        if len(authors) > maxauthors:
            authorstr = ', '.join(authors[:maxauthors]) + ' et al'
        else:
            authorstr = article.authors
    else:
        authorstr = article.authors
        glbls['nauthors'] = len(article.authors.split(','))

    firstauthor = Setting.get('name').value
    if not includeperiods:
        authorstr = authorstr.replace('. ', ' ').replace('.', ' ')
        firstauthor = firstauthor.replace('. ', ' ').replace('.', ' ')

    glbls['authors'] = authorstr
    glbls['firstauthor'] = firstauthor

    if abbrjournal:
        if article.journal in ABBREVIATIONS:
            glbls['journal'] = ABBREVIATIONS[article.journal]
        else:
            glbls['journal'] = article.journal
    else:
        glbls['journal'] = article.journal

    code = "def _refform_wrapfunc():\n"

    lines = s.split('\n')
    l = ''
    for line in lines:
        l += f'    {line}\n'

    code += l
    code += 'retval = _refform_wrapfunc()'

    exec(code, glbls)

    return glbls['retval']


