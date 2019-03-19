from setuptools import setup
from httpie_aws_authv4 import __version__

long_description = open('README.md').read()

setup(
    name='httpie-aws-authv4',
    description='AWS auth v4 plugin for HTTPie.',
    version=__version__,
    author='Aidan Rowe',
    author_email='aidanrowe@gmail.com',
    license='BSD',
    url='https://github.com/aidan-/httpie-aws-authv4',
    download_url='https://github.com/aidan-/httpie-aws-authv4',
    py_modules=['httpie_aws_authv4'],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_aws_authv4 = httpie_aws_authv4:AWSv4AuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=1.0.0',
        'aws_requests_auth>=0.4.0',
        'boto3>=1.9.0',
        'urllib3'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Environment :: Plugins',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
