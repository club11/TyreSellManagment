FROM python:3.9-slim

#RUN mkdir marketerexmachina_dir
#WORKDIR marketerexmachina_dir
#ADD . /marketerexmachina_dir/

WORKDIR /marketerexmachina_dir
COPY . /marketerexmachina_dir/

RUN pip install -r requirenments.txt

CMD python manage.py makemigrations \ 
&& python manage.py migrate \
&&  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='wlad').exists() or User.objects.create_superuser('wlad', 'club11@bk.ru', '11')" \
#&& python manage.py initialize_db \
&& python manage.py collectstatic --noinput \
&& gunicorn proj.wsgi:application -b 0.0.0.0:8001    


#&& gunicorn proj.wsgi:application -b -6 0.0.0.0:8001     #ipv6 MAYBE



 