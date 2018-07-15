FROM python:3.7-rc-stretch

WORKDIR /usr/src

ADD . /usr/src

RUN PYTHONPATH=$PYTHONPATH:/usr/src

# need pip install -e, python setup.py install didn't install requirements.txt :/
RUN pip install pbr wheel && pip install -e .