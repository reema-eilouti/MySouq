FROM python:3.7-alpine
RUN mkdir /mysouq
WORKDIR /mysouq
ADD requirements.txt .
RUN pip3 install -r requirements.txt
COPY app/ .
ENTRYPOINT ["sh"]