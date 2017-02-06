from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = open('README.md').read()

setup(
    name='httpie-aws-authv4',
    description='AWS auth v4 plugin for HTTPie.',
    version='0.1.0',
    author='Aidan Rowe',
    author_email='aidanrowe@gmail.com',
    license='BSD',
    url='https://github.com/aidan-/httpie-aws-authv4',
    download_url='https://github.com/aidan-/httpie-aws-authv4',
    py_modules=['httpie_aws_authv4'],
    zip_safe=False,
    long_description=long_description,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_aws_authv4 = httpie_aws_authv4:AWSv4AuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.9.7',
        'requests-aws>=0.1.8',
        'aws_requests_auth>=0.3.0',
        'boto3>=1.4.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Plugins',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
