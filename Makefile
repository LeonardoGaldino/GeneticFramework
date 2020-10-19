SHELL=/bin/bash
PATH_ARG:=$(path)
ifeq ($(PATH_ARG),)
PATH_ARG:=src/
endif

type-check:
	pipenv run mypy $(PATH_ARG)

format:
	pipenv run yapf -ri $(PATH_ARG)

.PHONY: type-check format