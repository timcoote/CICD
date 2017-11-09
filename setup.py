from distutils.core import setup

setup (name='updatedns',
        url = 'www.iotaa.co.uk',
        author = 'Tim Coote',
        author_email = 'tim.coote@differentis.com',
        version = '0.1',
        requires = ['godaddypy', 'boto3'],
        py_modules = ['update-dns'],
       )
