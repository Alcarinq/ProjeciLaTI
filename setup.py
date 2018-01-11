import os

from setuptools import setup, find_packages

requires = [
    'pyramid==1.8.3',
    'pyramid_debugtoolbar',
    'waitress',
    'pyramid_beaker',
    'pyramid_exclog',
    'pyramid_tm',
    'mako',
    'pyramid_mako',
    'psycopg2==2.7.1',
    'SQLAlchemy==1.1.7',
    'zope.sqlalchemy==0.7.7',
    "webhelpers==1.3",
    "python-dateutil==2.6.1",
    "webassets==0.9",
    "pyramid_webassets==0.7.1",
	'python_logstash==0.4.5'
    ]

setup(name='LaTI',
      version='1.0',
      description='LaTI',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Marcin Misztal',
      author_email='91mmisztal@gmail.pl',
      keywords='LaTI',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      message_extractors = {'lati': [
            ('**.py', 'python', None),
            ('templates/**.html', 'mako', None),
            ('static/**', 'ignore', None)]},
      entry_points="""\
      [paste.app_factory]
      main = lati:main
      """
)