.PHONY: run test clean

run:
	docker-compose up --build

test:
	docker-compose exec api pytest tests/ -v

clean:
	docker-compose down
	docker-compose rm -f
	docker system prune -f
