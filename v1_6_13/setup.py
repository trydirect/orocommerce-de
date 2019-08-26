#!/usr/bin/env python

import docker
import shutil

client = docker.from_env()

app = client.containers.get('orocommerce-de')
app.exec_run('mkdir -p ./app/logs && chmod 0777 -R ./app/logs && '
             'mkdir -p .app/cache && chmod 0777 -R .app/cache && mkdir -p web/web/js/translation && '
             'chmod 0777 -R web/web/js/translation/ && mkdir -p web/web/media && chmod 0777 -R web/web/media/ && '
             'mkdir -p web/web/uploads && chmod 0777 -R web/web/uploads/')
app.exec_run('chown -R orocommerce:orocommerce *')
app.exec_run('composer install --prefer-dist --no-dev')
shutil.copyfile('./configs/orocommerce/parameters.yml', './src/app/config/parameters.yml')
app.exec_run('rm -rf .app/cache/*')
args = " --organization-name='tes' " \
       "--user-name='test' --user-email='test' --application-url='http://localhost' " \
       "--user-firstname='test' --user-lastname='test " \
       "--user-password='test--sample-data='n' "
app.exec_run('chown -R orocommerce:orocommerce *')
print(app.exec_run('php ./app/console oro:install {} --drop-database --timeout=5800'.format(args)).output)
print(app.exec_run('rm -rf .app/cache/dev').output)
print(app.exec_run('rm -rf .app/cache/prod').output)
print(app.exec_run('php app/console cache:clear --env=prod').output)
print(app.exec_run('php app/console oro:platform:update --env=prod --force').output)
print(app.exec_run('php app/console cache:clear --env=prod').output)
print(app.exec_run('rm -f .app/install.php').output)
