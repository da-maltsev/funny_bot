# Funny bot project
     
Here I just try to discover how AI models can be useful for me. And do some implementation of these models with telegram bot. At this moment this bot can generate images and answer questions with chatgpt-3.5

## Installing on a local machine
This project requires python 3.10. Deps are managed by [pip-tools](https://github.com/jazzband/pip-tools)

Install requirements:

```bash
$ pip install --upgrade pip pip-tools
$ make
```

Run the script:

```bash
$ cd src && cp .env.example .env  # default environment variables
$ python main.py
```

Testing:
```bash
# run lint
$ make lint

# run unit tests
$ make test
```