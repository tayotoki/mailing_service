.PHONY: install migrate load_data run

install:
	@poetry install

migrate:
	@poetry run python manage.py migrate --check; \
    RET=$$?; \
    if [ $$RET -eq 0 ]; then \
        echo "No pending migrations. Skipping migration step."; \
    else \
        poetry run python manage.py migrate -q; \
    fi

load_data: migrate
	@poetry run python manage.py shell < db_procces.py

run: load_data
	@poetry run python manage.py runserver