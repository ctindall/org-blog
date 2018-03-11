release:
	echo cutting release for v$(v)
	sed -i "s/version\='.*'/version='$(v)'/" setup.py 
	git add .
	git commit -m"cutting release"
	python3 setup.py sdist upload -r pypi
