ins-terr:
	pip3 install terraform-local

start-localstack:
	docker-compose up


tf-init:
	tflocal init -upgrade

tf-plan:
	tflocal plan

tf-apply:
	tflocal apply


see_resources_as_graph:
#  see results in https://dreampuf.github.io/GraphvizOnline/
	tflocal graph



