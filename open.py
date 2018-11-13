# bad thing with python is:
# you have dependancies...

import requests
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from contextlib import closing
import wget

def main():
    # get user course number
    course_number = input("Δώσε κωδικό μαθήματος(πχ. DDI123): ")
    # create link string
    link = "https://opencourses.ionio.gr/modules/document/?course=" + course_number

    # soup = BeautifulSoup(open('./index.html').read(), 'html.parser') # read
    # from html file

    # get html page and create soup
    soup = BeautifulSoup(simple_get(link), 'html.parser')
    # print(soup)

    # get all <a> elements
    rows = soup.findAll('a', {'class': "fileURL fileModal"})

    # for every row, extract href attribute and append it to a list
    # print(rows)
    downloads = [row.attrs["href"] for row in rows]
    for file in downloads: # for every file
        print(file)
        filename = download_file(file) # download and store file


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

if __name__ == "__main__":
    main()
