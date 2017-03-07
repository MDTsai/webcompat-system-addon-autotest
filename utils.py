#!/usr/bin/python
import re
from requests import get

firefox_ftp_url = 'https://ftp.mozilla.org/pub/firefox/nightly/latest-mozilla-central/'
nightly_version_pattern = re.compile(b'firefox\-([a-z0-9\.]+)\.en\-US')


def download_firefox(url, platform):
    """
    Download firefox from given URL and save to filename by platform
    """
    filenames = {
        'win32': 'firefox.zip',
        'linux': 'firefox.tar.bz2',
        'darwin': 'firefox.dmg'
    }

    filename = filenames[platform]

    with open(filename, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

    return filename


def make_nightly_link(product, version, platform, locale):
    """
    Download links are different for localized versions
    """
    filenames = {
        'win32': 'win32.zip',
        'linux': 'linux-x86_64.tar.bz2',
        'darwin': 'mac.dmg'
    }
    filename = filenames[platform]

    return ('%s%s-%s.%s.%s' % (firefox_ftp_url, product, version, locale, filename))


def parse_version(source_file, version_pattern):
    """
    Parse version info from ftp page, get first version only
    """
    from urllib.request import urlopen
    response = urlopen(source_file).read()
    versions_match = version_pattern.finditer(response)
    version_match = next(versions_match)
    version = version_match.group(1)

    return version.decode("utf-8")


def parse_nightly_version():
    return parse_version(firefox_ftp_url, nightly_version_pattern)
