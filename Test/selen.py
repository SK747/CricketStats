from helium import *

url = 'https://www.cricbuzz.com/cricket-full-commentary/31623/rsa-vs-sl-1st-test-sri-lanka-tour-of-south-africa-2020-21'

browser = start_chrome(url, headless=True)

html = browser.page_source

print(html)