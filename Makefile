up:
	@docker-compose up -d --build

down:
	@docker-compose down

status:
	@docker-compose ps
web_it:
	@docker exec -ti web /bin/bash

log:
	@docker-compose logs

test:
	@docker-compose exec web python -m pytest

docker_start:
	@sudo service docker start

docker_stop:
	@sudo service docker start

docker_status:
	@docker ps

create_db:
	@docker-compose exec web python manage.py create_db

inspect volume:
	@docker volume inspect pred_foot_postgres_data