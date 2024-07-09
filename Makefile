.venv:
	pyenv local 3.10
	python3 -m venv .venv

jars/build/libs/spark-sql-kafka-build-all.jar:
	cd jars && ./gradlew shadowJar

.PHONY: install
install: .venv jars/build/libs/spark-sql-kafka-build-all.jar
	.venv/bin/pip3 install -q --upgrade pip
	.venv/bin/pip3 install -r requirements.txt

.PHONY: clean-jars
clean-jars:
	rm -rf jars/.gradle jars/build

.PHONY: clean
clean: clean-jars
	rm -rf .venv
