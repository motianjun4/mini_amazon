run:
	flask run --port 5001 --host 0.0.0.0
install:
	pip install -r requirements.txt
lint:
	pylint --disable=R,C,W ./app