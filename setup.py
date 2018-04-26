
#! /usr/bin/env python


from setuptools import setup
setup(
    name='mdx_ezcodeexample',
    version='1.0.0',
    author='Damian Zabawa',
    author_email='damian.zabawa@ez.no',
    description='Markdown extension which allows to insert code examples as HTML escaped code and rendered code',
    url='https://github.com/damianz5/mdx_ez_code_example',
    py_modules=['mdx_ez_code_example'],
    install_requires=['Markdown>=2.0',],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)

