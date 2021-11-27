build:
	docker-compose build

docker-run: build
	docker-compose up

docker-stop:
	docker-compose down

microk8s-import: build
	for s in cons pgsql prod redis server; do \
	  docker save dbz-$$s > dbz-$$s.tar; \
	  microk8s.ctr image import dbz-$$s.tar; \
	  rm dbz-$$s.tar; \
	done

microk8s-run: microk8s-import
	microk8s.kubectl apply -f kubernetes.yaml

microk8s-stop:
	microk8s.kubectl delete deployment --all
	for s in pgsql redis server; do \
	  microk8s.kubectl delete service dbz-$$s; \
	done
