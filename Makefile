dev-start:
	uv run manage.py runserver --settings=config.settings.dev 
dev-migrate:
	uv run manage.py migrate --settings=config.settings.dev 
dev-makemigrations:
	uv run manage.py makemigrations --settings=config.settings.dev