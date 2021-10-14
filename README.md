# databand_project
Home Assignment Databand.ai

Written by Eden Avitan following a home assignment.

To run this code run: app.py file.
In the appropriate port, an HTTP (Flask) server will be for your service.

This server has 2 endpoints:
1) crawl/{url_path} - This endpoint will be crawl to the given URL, will save the contents of the HTML file of the main given page in the database SQLite (local storage), 
and will crawl to the all existing links in it and return them (they can be seen in the browser at the appropriate address).
For example:
We would like to use endpoint crawl/{url_path}.
We would crawl into a given page (Google for example) so that:
url_path = https://www.google.com/
Therefore, our URL in the browser will be:
http://localhost:PORT_Number/crawl/https://www.google.com/
for example: 
http://127.0.0.1:5000/crawl/https://www.google.com/


2) last_seen/{url_path} - In the endpoint, we can perform in the same way as the first endpoint a check when we crawled to a given URL (when was the last seen).

In the browser:
http://localhost:PORT_Number/last_seen/https://www.google.com/

For example:
http://127.0.0.1:5000/last_seen/https://www.google.com/

And the browser will show us the last time we crawled to this address.
