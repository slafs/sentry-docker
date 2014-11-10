#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
import sys

# Bootstrap the Sentry environment
from sentry.utils.runner import configure
configure()

# Do something crazy
from sentry.models import Team, Project, ProjectKey, User


def create_team(admin_username, team_name):
    user = User.objects.get(username=admin_username)
    team, new = Team.objects.get_or_create(name=team_name,
                                           defaults={'owner': user})
    return team, new


def create_project(team_name, project_name):
    team = Team.objects.get(name=team_name)
    project, new = Project.objects.get_or_create(name=project_name, team=team,
                                                 defaults={'owner': team.owner})

    return project, new


def enforce_key(project, key_string):
    key = ProjectKey.objects.get(project=project)
    public, secret = key_string.split(':')
    key.public_key = public
    key.secret_key = secret
    key.save()


def print_dsn(project):
    key = ProjectKey.objects.get(project=project)
    print('=' * 50)
    print('You have a project called {0}. You can use the following DSN'
          .format(project.name))
    print('SENTRY_DSN = "{0}"'.format(key.get_dsn()))
    print('=' * 50)


def main():
    '''CLI usage:

    to create a team::

        python create_team_or_project.py team adminusername teamname

    to create a project::

        python create_team_or_project.py project teamname projectname

    to modify key for a project::

        python create_team_or_project.py key teamname projectname public:secret
    '''
    command = sys.argv[1]
    if command == 'team':
        admin_username = sys.argv[2]
        team_name = sys.argv[3]
        team, _ = create_team(admin_username, team_name)
    elif command in ('project', 'key'):
        team_name = sys.argv[2]
        project_name = sys.argv[3]
        project, proj_created = create_project(team_name, project_name)

        if command == 'key':
            key = sys.argv[4]
            enforce_key(project, key)
            print_dsn(project)
        elif proj_created is True:
            print_dsn(project)

if __name__ == '__main__':
    main()
