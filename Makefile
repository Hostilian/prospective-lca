.PHONY: demo test validate-demo validate-production site docker-build docker-run clean

PYTHON ?= python3
DEMO_OUT ?= exports/demo

demo:
	$(PYTHON) -m app.cli demo --out $(DEMO_OUT)

test:
	$(PYTHON) -m compileall -q app tests
	$(PYTHON) -m unittest discover -s tests -v

validate-demo:
	$(PYTHON) -m app.cli validate --mode demo

validate-production:
	@set -e; \
	status=0; $(PYTHON) -m app.cli validate --mode production || status=$$?; \
	if [ "$$status" -ne 2 ]; then \
		echo "Expected the synthetic project to be blocked with exit code 2; got $$status"; \
		exit 1; \
	fi; \
	echo "Production gate correctly blocked the unresolved synthetic project."

site:
	rm -rf _site
	$(PYTHON) -m app.cli demo --out _site

docker-build:
	docker build --tag awam-prospective-lca-workbench:local .

docker-run:
	docker run --rm --publish 8765:8765 awam-prospective-lca-workbench:local

clean:
	rm -rf _site exports/demo

