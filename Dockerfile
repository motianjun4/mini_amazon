FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN make install
RUN make lint
CMD make run
EXPOSE 5001
