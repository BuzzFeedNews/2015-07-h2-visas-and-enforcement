WHD_DB_PARTS = $(wildcard data/whd-compressed/*)

default:
	@echo No default target

data/whd-enforcement-database: $(WHD_DB_PARTS)
	cat $(WHD_DB_PARTS) | tar -xzvf - -C data

OFLC_FETCHERS = scripts/fetch-oflc-recent-data.py scripts/fetch-oflc-archived-data.py
data/oflc-decisions/raw: $(OFLC_FETCHERS)
	mkdir -p $@
	find $@ -type f -exec rm {} \;
	./scripts/fetch-oflc-recent-data.py $@
	./scripts/fetch-oflc-archived-data.py $@

data/oflc-decisions/processed: data/oflc-decisions/raw scripts/combine-oflc-data.py
	mkdir -p $@
	find $@ -type f -exec rm {} \;
	./scripts/combine-oflc-data.py data/oflc-decisions/raw > $@/oflc-decisions.csv

output/certification-lists: data/oflc-decisions/processed scripts/generate-certification-lists.py
	mkdir -p $@
	find $@ -type f -exec rm {} \;
	./scripts/generate-certification-lists.py

.PHONY: notebooks clean all
notebooks:
	./scripts/run-all-notebooks.sh

clean:
	rm -rf data/whd-enforcement-database
	rm -rf data/oflc-decisions/processed
	find output -type f -exec rm {} \;

all: clean \
	data/whd-enforcement-database \
	data/oflc-decisions/processed \
	output/certification-lists \
	notebooks
	
