JS_TESTER = /usr/bin/vows
PEG_COMPILER = /usr/bin/pegjs

.PHONY: test

%.js: %.peg Makefile
	$(PEG_COMPILER) < $< > $@

all: \
	lib/cube/event-expression.js \
	lib/cube/metric-expression.js

test: all
	@$(JS_TESTER)
