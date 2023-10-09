# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:focal
ENV SECRET_KEY=insecure-t_^p_ilh%2+9i%_o+de-5a0dg$sth8zqtq#yl4eq@!j_%=-4p$
ENV DEBUG=true
ENV DATABASE_URL=postgres://efit:Tech2023db@34.67.50.41/efitdb
ENV DJANGO_ENVIRONMENT=production
# update packages
RUN apt-get update

# install required packages
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y python3 python3-dev python3-setuptools python3-pip python3-software-properties python3-testresources
RUN apt-get install -y supervisor

# install latest stable nginx
RUN apt-get install -y nginx-full

# install uwsgi now because it takes a little while
RUN pip install uwsgi
RUN apt-get -y install uwsgi uwsgi-plugin-python3 
# install our code
ADD . /gambling/
ENV PYTHONPATH=/gambling/:$PYTHONPATH
# setup all the configfiles
RUN service nginx stop

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /gambling/nginx.conf /etc/nginx/sites-enabled/
RUN ln -s /gambling/supervisor-app.conf /etc/supervisor/conf.d/
WORKDIR /gambling
# run pip install
RUN pip install pipenv
RUN pip install -U pip
RUN pip install -r requirements.txt
#RUN python3 /gambling/api/manage.py syncdb
# install django, normally you would remove this step because your project would already
# be installed in the code/app/ directory
EXPOSE 8080
CMD ["supervisord", "-n"]