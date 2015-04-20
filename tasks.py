from invoke import run, task


@task
def build():
    run('python setup.py build')
    run('python setup.py sdist')
    run('python setup.py bdist_wheel')


@task
def install():
    run('python setup.py build')
    run('python setup.py install')


@task
def pypi_upload():
    run('python setup.py sdist upload')
    run('python setup.py bdist_wheel upload')
