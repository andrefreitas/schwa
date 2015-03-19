from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

setup(name='Schwa',
      version='0.1-dev',
      description='Git Repositories Mining',
       entry_points = {
        "console_scripts": ['schwa = schwa.schwa:main']
        },
      author='Andre Freitas',
      author_email='p.andrefreitas@gmail.com',
      url='https://github.com/andrefreitas/schwa',
      packages=['schwa', 'schwa.analysis', 'schwa.extraction', 'schwa.parsing', 'schwa.repository', 'schwa.web'],
      install_requires=reqs
)