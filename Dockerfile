FROM python:3.10.1-bullseye
WORKDIR /usr/src/app
COPY . .
RUN make install
RUN make lint
CMD make run
EXPOSE 5000
