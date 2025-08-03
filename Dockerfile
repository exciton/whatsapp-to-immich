FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ADD https://github.com/simulot/immich-go/releases/download/v0.27.0/immich-go_Linux_x86_64.tar.gz .
RUN tar xz -f immich-go_Linux_x86_64.tar.gz immich-go -C /usr/bin/

COPY . .

RUN crontab cronfile

CMD [ "crond", "-f" ]
#CMD [ "sh" ]
