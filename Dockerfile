
FROM python:3.6-alpine

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -U pip \
    && pip install -r /tmp/requirements.txt

COPY . /code
WORKDIR /code

CMD ./manage.py run

EXPOSE 5010



