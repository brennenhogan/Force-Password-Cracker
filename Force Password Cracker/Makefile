test:
	@$(MAKE) -sk test-all

test-all:	test-scripts test-hulk

test-scripts:
	curl -sLOk https://gitlab.com/nd-cse-20289-sp19/cse-20289-sp19-assignments/raw/master/homework05/test_hulk.sh
	curl -sLOk https://gitlab.com/nd-cse-20289-sp19/cse-20289-sp19-assignments/raw/master/homework05/hashes.txt
	chmod +x test_hulk.sh

test-hulk:
	./test_hulk.sh
