SHELL := /bin/bash

run:
	flask run --port 5001 --host 127.0.0.1
install:
	pip install -r requirements.txt
lint:
	pylint --disable=R,C,W ./app
gen_db_data:
	cd db && python3 gen.py
load_db_data:
	cd db && source load.sh