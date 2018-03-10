FROM python:last
ADD ./security-center.pyz /code/security-center.pyz
ADD ./static /code/static
ADD ./templates /code/templates
ADD ./requirements/requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt