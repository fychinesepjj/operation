# globals
from fabric.api import env, run, sudo, require, put, get, cd, lcd, local, settings
from fabric.contrib.files import exists
from fabric.context_managers import prefix
from fabric.colors import yellow, green, red

env.project_name = 'sckpu'


# environments
def sckpu_server():
    "Use the local virtual server"
    env.hosts = ['jjpan@121.42.48.136:22']
    env.remote_path = '/var/app'
    env.user = 'jjpan'
    env.virtualenv_setting = 'virtualenvwrapper.setting.sh'
    env.virtualhost_remote_path = env.remote_path + "/virtualenvs"
    env.project_log_dir = env.remote_path + '/log/' + env.project_name
    env.project_virtualenv = '%s_env' % env.project_name
    env.project_release_dir = '%s/releases/%s' % (env.remote_path, env.project_name)


# tasks
def test():
    "Run the test suite and bail out if it fails"
    print yellow("test")
    #run('cd %(remote_path)s/releases/%(release)s && tar zxf ../../packages/%(release)s.tar.gz' % env)
    #sudo('cd %(remote_path)s/releases;ln -s %(release)s current' % env)
    #run('workon project_env && echo "ok"')


def setup_virtualenvwrapper():
    with cd('~'):
        with settings(warn_only=True):
            result = run("cat .profile |grep 'source.*virtualenvwrapper.setting.sh'")
        if result.failed:
            print yellow('virtualenvwrapper settings not in .profile, system will create...')
            profile_setting = 'source %s/%s' % (env.remote_path, env.virtualenv_setting)
            sudo('echo "%s" >> .profile' % profile_setting)
        else:
            print result
        run('mkvirtualenv %s' % env.project_virtualenv)
    run('echo "WORKON_HOME:$WORKON_HOME"')


def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    print green("\nBegin to setup project: %s" % env.project_name)
    require('hosts', provided_by=[local])
    require('remote_path')
    #sudo('apt-get install python-dev')
    #sudo('aptitude install -y python-setuptools')
    #sudo('easy_install pip')
    #sudo('pip install virtualenv')
    #sudo('pip install virtualenvwrapper')
    sudo('mkdir -p %s' % env.remote_path)
    sudo('mkdir -p %s' % env.project_log_dir)
    sudo('chmod -R  777 %s' % env.remote_path)
    with cd(env.remote_path):
        if not exists(env.virtualenv_setting):
            put(env.virtualenv_setting, env.remote_path)
            sudo('chmod 777 %s' % env.virtualenv_setting)
        else:
            print yellow('virtualenv setting has been exists.')
        setup_virtualenvwrapper()
        run('mkdir -p releases/%(project_name)s; mkdir -p packages/%(project_name)s;' % env)
    deploy()


def deploy():
    """
    Deploy the latest version of the site to the servers, install any
    required third party modules, install the virtual host and
    then restart the webserver
    """
    print green("\nBegin to deploy project: %s" % env.project_name)
    require('hosts', provided_by=[local])
    require('remote_path')
    import time
    env.release = '%s_%s' % (env.project_name, time.strftime('%Y%m%d%H%M%S'))
    upload_tar_from_git()
    install_requirements()
    symlink_current_release()
    #setting_server()
    restart_webserver()


def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    """
    print green("\nBegin to rollback current deployment")
    require('hosts', provided_by=[local])
    require('remote_path')
    with cd(env.project_release_dir):
        run('mv current _previous;mv previous current;mv _previous previous;')
        restart_webserver()


def upload_tar_from_git():
    print green("\nCreate an archive from the current Git master branch and upload it")
    require('release', provided_by=[deploy, setup])
    release_tar = '%s.tar.gz' % env.release
    local('git archive --format=tar master | gzip > /tmp/%s' % release_tar)
    run('mkdir -p %(project_release_dir)s/%(release)s' % env)
    put('/tmp/%s' % release_tar, '%(remote_path)s/packages/%(project_name)s' % env)
    run('cd %(project_release_dir)s/%(release)s && tar zxf %(remote_path)s/packages/%(project_name)s/%(release)s.tar.gz' % env)
    local('rm /tmp/%s' % release_tar)


def install_requirements():
    print green("\nInstall the required packages from the requirements file using pip")
    require('release', provided_by=[deploy, setup])
    requirements = '%(project_release_dir)s/current/requirements.txt' % env
    with prefix('workon %s' % env.project_virtualenv):
        if exists(requirements):
            run('pip install -r %s' % requirements)
        else:
            print yellow('File %s not exists, continue deploy.' % requirements)


def symlink_current_release():
    "Symlink our current release"
    print green("\nSymlink our current release")
    require('release', provided_by=[deploy, setup])
    run('cd %(project_release_dir)s;rm -rf previous;mv current previous;mv %(release)s current' % env)


def migrate():
    "Update the database"
    require('project_name')
    run('cd $(remote_path)/releases/current/$(project_name);  ../../../bin/python manage.py syncdb --noinput')


def setting_server():
    "Add the virtualhost file to nginx, add crond file ..."
    require('project_release_dir')
    current_dir = '%(project_release_dir)s/current/scripts' % env
    setting_script = '%s/%s' % (current_dir, 'setting_server.sh')
    if exists(current_dir):
        with cd(current_dir):
            if exists(setting_script):
                sudo(setting_script)
            else:
                print yellow("Fail: setting_server.sh file not exists in remote server %s dir." % current_dir)
    else:
        print red("Fail: %s not exists in remote server, please ensure you have run <setup> cmd before <deploy>." % current_dir)


def restart_webserver():
    "Restart the web server"
    local('echo "restart server."')
