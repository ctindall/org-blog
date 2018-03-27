release:
	echo cutting release for v$(v)
	sed -i "s/version\='.*'/version='$(v)'/" setup.py 
	git add .
	git commit -m"cutting release v$(v)"
	git tag v$(v) HEAD
	python3 setup.py sdist upload -r pypi
	git push origin master
	git push github master
	git push --tags origin
	git push --tags github

test-release:
	python3 setup.py install
