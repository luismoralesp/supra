from distutils.core import setup
import os

# version (shape.function.path)
# python setup.py sdist upload
setup(
	name='supra',
	version='1.0.14',
	packages=['supra', 'supra.templatetags'],
	url='https://github.com/luismoralesp/supra',
	author="Luis Miguel Morales Pajaro",
	author_email="luismiguel.mopa@gmail.com",
	licence="Creative Common",
	description="It's an easy JSON services generator",
	platform="Linux",
	zip_safe=False,
	include_package_data=True,
	package_data={'supra': ['templates/supra/*.html']},
)