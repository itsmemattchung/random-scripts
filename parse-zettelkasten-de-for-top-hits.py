# Quick and dirty script to parse through forum pages on zettelkasten.de forum
# page. Only odd thing was that the unit of view count can be in thousands (i.e.
# appended with a 'k').

import os
import sys
from collections import namedtuple

import bs4
from bs4 import BeautifulSoup

PageMetaData = namedtuple('PageMetaData', 'title url views')

def parse_for_view_count(text):
    # Example inputs:
    #  1.1K
    #  300

    text_lowered = text.lower()

    if text_lowered.endswith('k'):
        # e.g. 1.1K
        view_count = float(text.lower().rstrip('k'))
        return int(view_count * 1000)

    else:
        return int(text)

def page_metadata_from_element_tag(tag):
    assert isinstance(tag, bs4.element.Tag)

    a_href = tag.find('a')

    assert(a_href)

    title = a_href.text
    url = a_href['href']

    assert title and url
    assert url.startswith('https')

    span_number = tag.find('span', {'class': 'Number'})
    assert span_number
    # ValueError: invalid literal for int() with base 10: '1.1K'
    views_count = int(parse_for_view_count(span_number.text))
    return PageMetaData(title, url, views_count)



if __name__ == "__main__":
    program_name = sys.argv[0]
    if len(sys.argv[1:]) != 1:
        print("Error. Requires input file name")
        sys.exit(1)
    filename = sys.argv[1]

    # check if file exists

    if not os.path.exists(filename):
        print("Error. %s does not exist" % filename)
        sys.exit(1)

    with open(filename) as fh:

        soup = BeautifulSoup(fh, 'html.parser')
        discussions = soup.find_all('div', {'class': 'ItemContent Discussion'})
        assert discussions and len(discussions) > 0

        for discussion in discussions:

            page_metadata = page_metadata_from_element_tag(discussion)
            print("%s,%s,%s" %(page_metadata.title,page_metadata.url,page_metadata.views))

