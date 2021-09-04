import sys
import os
import argparse
import tempfile
import webbrowser
from bs4 import BeautifulSoup
import re

from urllib.request import urlopen

parse = argparse.ArgumentParser(description='Novel Reformat URL arguments')

parse.add_argument('URL',
                   metavar='url',
                   type=str,
                   help='the url to the novel chapter')

args = parse.parse_args()

URL = args.URL

# TODO: add catch for bad URL
# if not os.path.isdir(URL):
#     print('The URL does not exist')
#     sys.exit()
print(URL)

# with urlopen(URL) as page_text:
#     print(page_text.read().decode('utf-8'))
#
#     html = page_text.read().decode('utf-8')
#
#     with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
#         url = 'file://' + f.name
#         f.write(html)
#     webbrowser.open(url)
# # print(data)

html = urlopen(URL).read()
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.prettify()

#TODO: check for [ /n ] type of T/N
text = re.sub(r"[\[].*?[\]]", "", text, flags=re.DOTALL)
print(text)

# break into lines and remove leading and trailing space on each
# lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
# text = '\n'.join(chunk for chunk in chunks if chunk)

# print(text)
with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    test_url = 'file://' + f.name
    f.write(text)
webbrowser.open(test_url)
