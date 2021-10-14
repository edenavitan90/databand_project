# databand_project
Home Assignment Databand.ai
 <br> 
 <br> Written by Eden Avitan following a home assignment.
 <br> 
 <br> To run this code run: app.py file.
 <br> In the appropriate port, an HTTP (Flask) server will be for your service.
 <br> 
 <br> This server has 2 endpoints:
 <br> 1) crawl/{url_path} - This endpoint will be crawl to the given URL, will save the contents of the HTML file of the main given page in the database SQLite (local storage), 
 <br> and will crawl to the all existing links in it and return them (they can be seen in the browser at the appropriate address).
 <br> For example:
 <br> We would like to use endpoint crawl/{url_path}.
 <br> We would crawl into a given page (Google for example) so that:
 <br>url_path = https://www.google.com/
 <br> Therefore, our URL in the browser will be:
 <br> http://localhost:PORT_Number/crawl/https://www.google.com/
 <br> for example: 
 <br> http://127.0.0.1:5000/crawl/https://www.google.com/
 <br> 

 <br> 2) last_seen/{url_path} - In the endpoint, we can perform in the same way as the first endpoint a check when we crawled to a given URL (when was the last seen).
 <br> In the browser:
 <br> http://localhost:PORT_Number/last_seen/https://www.google.com/
 <br> For example:
 <br> http://127.0.0.1:5000/last_seen/https://www.google.com/
 <br> And the browser will show us the last time we crawled to this address.
