i:
	virtualenv venv
	source venv/bin/activate; \
	pip install -r requirements.txt

run:
	source venv/bin/activate; \
	python3 main.py
