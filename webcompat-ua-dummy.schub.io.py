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
    binary = FirefoxBinary("./firefox/firefox")
    # Create Firefox WebDriver
    firefox = webdriver.Firefox(firefox_binary=binary)

    # Visit webcompat-ua-dummy, verify title and page
    firefox.get("http://webcompat-ua-dummy.schub.io/")

    assert "Unsupported browser" not in firefox.title
    assert "Please use Chrome to visit this website!" not in firefox.page_source

    firefox.quit()
