FROM python:3.9-slim

#RUN mkdir marketerexmachina_dir
#WORKDIR marketerexmachina_dir
#ADD . /marketerexmachina_dir/

WORKDIR /marketerexmachina_dir
COPY . /marketerexmachina_dir/

#RUN pip install psycopg2-binary
RUN pip install -r requirenments.txt

CMD python manage.py makemigrations \ 
&& python manage.py migrate \
&&  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('wlad', 'club11@bk.ru', '11')" \
#&& python manage.py initialize_db \
&& python manage.py collectstatic --noinput \
#&& python manage.py runserver 0.0.0.0:8000  
&& gunicorn proj.wsgi:application -b 0.0.0.0:8001  


# CMD gunicorn proj.wsgi:application -b 0.0.0.0:8000  