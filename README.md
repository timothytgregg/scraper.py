
# Scraper.py

Built for scraping contact information from tens of thousands of NGO pages.

## Process

main.py generates a retrieved.data.log, 

which contains a dictionary of {organization_name:{'email':'foo@bar.com','website':'example.com',...},...}

which dict-to-csv.py converts into a .csv file

### Dependencies:

`pip install beautifulSoup`

`pip install fake_useragent`

secrets.py contains the hidden url.
