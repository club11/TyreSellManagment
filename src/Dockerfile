FROM python:3.9-slim

RUN mkdir codewww
WORKDIR codewww

ADD . /codewww/

RUN pip install psycopg2-binary
RUN pip install -r requirenments.txt

CMD python manage.py makemigrations \ 
&& python manage.py migrate \
#&& python manage.py initialize_db \
&& python manage.py collectstatic \
#&& python manage.py runserver 0.0.0.0:8000  
&& gunicorn proj.wsgi:application -b 0.0.0.0:8000  


# CMD gunicorn proj.wsgi:application -b 0.0.0.0:8000  