# Words counter api

This is the README of the Words Counter Crawling API. In order to create the API, I have decided to use FastAPI along with BeautifulSoup4 to scrape the HTML content from the given url.

## How to run the project

In order to run the project locally, there is 2 ways. You can either run locally on your machine or you can build the DOcker image based on the provided  Dockerfile and run the Docker container locally.

### Run the project locally

To be able to setup the project locally, you have to setup the virtual environment first and install the dependencies within it.

Create the virtual environment (I am using virtualenv here, but any other tool like pipenv can be used)
```
$ python -m virtualenv venv 
```

Activate the virtual environment into you shell
```
$ source venv/bin/activate
```

Install the dependencies
```
$ pip install -r requirements.txt
```

Then to run the project, we will use the `uvicorn` server to expose the api.

```
$ PYTHONPATH=app uvicorn api:app
```

### Run the project using Docker

Please ensure to have Docker installed on your machine before proceeding.

Build the Docker image
```
$ docker build -t words_count_api .
```

Run a Docker container
```
$ docker run --network host words_count_api

```
### Run the unit tests locally

If you want to run the automated tests locally, you will have to setup a virtual environment and install the dependencies from `requirements.txt` and then run the following command:

```
$ PYTHONPATH=app python -m pytest

```


### Access to the api

By default, the Docker container exposes the API on the port 8000.

To know more about the API itself, you can access to `https://http://127.0.0.1:8000/docs` via your web browser
(alternatively, you may prefer to got to `http://127.0.0.1:8000/redoc` for the same API documentation with a slight diferrent presentation).

Example of valid queries:
- `http://127.0.0.1:8000/words_count/https://bbc.co.uk?order=alphabetical`
- `http://127.0.0.1:8000/words_count/https://dw.com?order=asc_count`
- `http://127.0.0.1:8000/words_count/https://cnn.com?order=desc_count`

## Technical decisions

## Areas of improvement
