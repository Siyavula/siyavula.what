from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='siyavula.what',
      version=version,
      description="siyavula.what",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Upfront Systems',
      author_email='rijk@upfrontsystems.co.za',
      url='https://github.com/Siyavula/siyavula.what',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['siyavula'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity',
          'plone.namedfile [blobs]',
          # -*- Extra requirements: -*-
      ],
      extras_require={
        'test': [
          'plone.app.testing',
        ],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      # The next two lines may be deleted after you no longer need
      # addcontent support from paster and before you distribute
      # your package.
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],

      )
