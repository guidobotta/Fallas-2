run:
	docker-compose -f docker-compose.yaml up -d --build
.PHONY: run

stop:
	docker-compose -f docker-compose.yaml stop -t 1
	docker-compose -f docker-compose.yaml down
.PHONY: stop

logs:
	docker-compose logs -f
.PHONY: logs

