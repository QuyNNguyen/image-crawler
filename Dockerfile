FROM python:3




ADD act1-2.py /
RUN pip install beautifulsoup4
CMD [ "python", "./act1-2.py" ]