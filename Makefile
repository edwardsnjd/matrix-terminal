# Sanity
# From: https://tech.davis-hansson.com/p/make/

SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# Convenience targets

help:
	@echo "Targets:"
	@echo "- help (default) = print this info"
	@echo "- test = run unit tests"
	@echo "- check = type check using mypy"
.PHONY: help

test:
	@python3 -m unittest discover -s src \
		&& echo "-- ✅ Tests passed ✅ --" \
		|| echo "-- ❌ Tests failed ❌ --"
.PHONY: test

check:
	@cd src && mypy main.py
.PHONY: check
