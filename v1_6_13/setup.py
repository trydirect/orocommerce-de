#!/usr/bin/env python

import docker
import shutil
import time

client = docker.from_env()

app = client.containers.get('orocommerce-de')
app.exec_run('mkdir -p ./app/logs && chmod 0777 -R ./app/logs && '
             'mkdir -p .app/cache && chmod 0777 -R .app/cache && mkdir -p web/web/js/translation && '
             'chmod 0777 -R web/web/js/translation/ && mkdir -p web/web/media && chmod 0777 -R web/web/media/ && '
             'mkdir -p web/web/uploads && chmod 0777 -R web/web/uploads/')
app.exec_run('chown -R orocommerce:orocommerce *')
# print(app.exec_run('composer install --prefer-dist --no-dev').output)
shutil.copyfile('./configs/orocommerce/parameters.yml', './src/app/config/parameters.yml')
app.exec_run('rm -rf .app/cache/*')
args = " --organization-name='tes' " \
       "--user-name='test' --user-email='test' --application-url='http://localhost' " \
       "--user-firstname='test' --user-lastname='test " \
       "--user-password='test--sample-data='n' "
app.exec_run('chown -R orocommerce:orocommerce *')
app.exec_run('php ./app/console oro:install {} --drop-database --timeout=12800'.format(args), detach=True)
time.sleep(20*60)  # expect 20 mins for oro install
proc = app.exec_run('ps aux |grep php ./app/console oro:install').output
if 'oro:install' in proc:
    time.sleep(60 * 20)  # expect 20 mins for oro install
print(app.exec_run('rm -rf .app/cache/dev').output)
print(app.exec_run('rm -rf .app/cache/prod').output)
print(app.exec_run('php app/console cache:clear --env=prod').output)
print(app.exec_run('php app/console oro:platform:update --env=prod --force').output)
print(app.exec_run('php app/console cache:clear --env=prod').output)
print(app.exec_run('rm -f .app/install.php').output)
