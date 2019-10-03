# News Aggregator
Restful service that aggregates news from News API and Reddit and list them with search functionality.

# ABOUT
News Aggregator is a backend server written to aggregates articles. It uses Django Rest Framework to list all articles from News API and Reddit.

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

## Installing
`Clone or download the project`

### Navigate to the news folder
`cd path/to/news`

### Activate the virtual environment
`source env/bin/activate`

### Install required packages
`pip install -r /path/to/requirements.txt`

### Navigate to the rest app
`cd /src/news/`

### Run server
`python manage.py runserver`

### List aggregated news
Open your browser or Postman, paste the following URL: `http://127.0.0.1:8000/api/news/`

### Search aggregated news
Open your browser or Postman, paste the following URL: `http://127.0.0.1:8000/api/news/`

# Running the tests
### Run the following command
`Python manage.py test`

