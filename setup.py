from setuptools import setup, find_packages

setup(name='csvmanipulator',
      version='0.1',
      description='csvmanipulator',
      long_description="Process some CSVs with useful functions and render another CSV",
      classifiers=[
        "Programming Language :: Python",
        ],
      author='Leo Cavaille',
      author_email='leo@cavaille.net',
      url='',
      keywords='csv manipulation',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      entry_points="""\
      [console_scripts]
      csvmanip = csvmanipulator:main
      """,
)
