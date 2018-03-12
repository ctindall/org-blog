release:
	echo cutting release for v$(v)
	sed -i "s/version\='.*'/version='$(v)'/" setup.py 
	git add .
	git commit -m"cutting release"
	git tag v$(v) HEAD
	python3 setup.py sdist upload -r pypi

test-release:
	python3 setup.py install
