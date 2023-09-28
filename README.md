## Python Books API

Backend API application to perform CRUD operations on books and authors


### Live Demo

[http://python-books-api-env.eba-m6ybttk3.us-east-2.elasticbeanstalk.com](http://python-books-api-env.eba-m6ybttk3.us-east-2.elasticbeanstalk.com)


### Technical Breakdown

- Language: Python 3.11.3
- API Framework: Flask API
- Testing Framework: Pytest
- Database: MongoDB


### Setup

1. Make sure you have Python and PIP installed:

&emsp;&emsp;[Download it from python.org](https://www.python.org/downloads/)

2. Install packages and dependencies of the application:

```
pip install -r requirements.txt
```

3. Start a local API server at `http://localhost:4000`:

```
python main.py
```

&emsp;&emsp;
NOTE: To setup and populate your database you can run this command inside **data** directory:

```
python setup.py
```

NOTE: To run tests you can run this command inside **tests** directory:

```
pytest api-tests.py
```


&emsp;&emsp;
#### Developer

[Dariana Sanchez](https://www.linkedin.com/in/darianamsanchez/)