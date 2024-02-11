.PHONY: install migrate load_data run

install:
	@poetry install

migrate:
	@poetry run python manage.py migrate --check; \
    RET=$$?; \
    if [ $$RET -eq 0 ]; then \
        echo "No pending migrations. Skipping migration step."; \
    else \
        poetry run python manage.py migrate; \
    fi

load_data: migrate
	@poetry run python manage.py shell < db_procces.py

check_cron: load_data
	@if ! poetry run python manage.py crontab show | grep -q "mailing.cron.start_mailing_crons"; then \
        echo "Cron task does not exist"; \
        echo "Adding cron task"; \
        poetry run python manage.py crontab add; \
    else \
        echo "Cron task exists"; \
    fi

run: check_cron
	@poetry run python manage.py runserver