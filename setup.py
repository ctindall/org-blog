from setuptools import setup

setup(name='orgblog',
      version='',
      description='easy web publishing with org-mode files',
      url='http://github.com/ctindall/org-blog',
      author='Cameron Tindall',
      author_email="cam@tindall.space",
      license='GPL',
      packages=['orgblog'],
      zip_safe=False,
      scripts=['bin/orgblog'],
      install_requires = [
          "flask",
          "pystache"
      ])
