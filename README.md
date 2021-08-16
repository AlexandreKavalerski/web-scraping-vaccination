# Web Scraping - Covid Vaccination at Palmas

My personal python web scraping to notify (whatsapp and mail) when the city of Palmas-TO releases vaccination group age

## Setup

1. run `pip install -r requirements.txt` to install python dependencies
2. create a `.env` file according to `.env.example` vars
3. run `python index.py` (alternatively you can schedule a script to run it periodically)

### Dependencies

To correctly set dependencies and keys at `.env` file,  take a look at:
* [Gmail’s Application-Specific Password](https://support.google.com/accounts/answer/185833?hl=en)
* [Twilio account sid and auth token](https://www.twilio.com/console)