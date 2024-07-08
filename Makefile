.venv:
	pyenv local 3.10
	python3 -m venv .venv

.PHONY: install
install: .venv
	.venv/bin/pip3 install -q --upgrade pip
	.venv/bin/pip3 install -r requirements.txt
	cd jars && ./gradlew shadowJar

.PHONY: clean
clean:
	rm -rf .venv jars/.gradle jars/build
