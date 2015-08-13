from setuptools import setup, find_packages

setup(
    name='django-edtf',
    version='0.1.0',
    description='A Django app for the validation of dates in the Extended Date Time Format.',
    long_description=('Please visit https://github.com/unt-libraries/django-edtf'
                      ' for the latest documentation.'),
    install_requires=['edtf-validate>=1.0.0'],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    url='https://github.com/unt-libraries/django-edtf',
    author='University of North Texas Libraries',
    license='BSD',
    keywords=['django', 'edtf', 'validate', 'datetime'],
    classifiers=[
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ]
)
