FROM python:alpine3.17
ADD . .
RUN apk update && apk add curl && apk add firefox-esr && \
curl -L https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz | tar xz -C /usr/local/bin 

RUN pip install -r requirements.txt
CMD ["python3","echelon.py"]
RUN ls
