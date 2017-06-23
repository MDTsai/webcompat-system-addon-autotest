#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from shutil import unpack_archive
import utils


if __name__ == "__main__":
    from sys import platform
    # Get nightly URL
    nightly_url = utils.make_nightly_link("firefox", utils.parse_nightly_version(), platform, "en-US")

    # Download nightly
    nightly_path = utils.download_firefox(nightly_url, platform)

    # Extract to folder
    unpack_archive(nightly_path)

    # Create a Firefox Binary from folder
    binary = FirefoxBinary(utils.get_firefox_binary_path(platform))
    # Create Firefox WebDriver
    firefox = webdriver.Firefox(firefox_binary=binary)

    # Visit icloud.com, verify title and page
    firefox.implicitly_wait(30)
    firefox.get("https://www.icloud.com/keynote/0hmu8sUZRot_9XJACva_hdnKA#DocGroup%5FLabeling%5Fin%5FQuantum%5FDOM")

    assert u"Your browser isn’t fully supported." not in firefox.page_source

    firefox.quit()
