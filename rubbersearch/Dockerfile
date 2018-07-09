FROM python:3.7-rc-stretch

WORKDIR /usr/src

ADD . /usr/src

RUN PYTHONPATH=$PYTHONPATH:/usr/src

RUN pip install --update pip && pip install rubbersearch/requirements.txt
