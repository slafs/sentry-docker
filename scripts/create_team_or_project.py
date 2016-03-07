#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
import sys

# Bootstrap the Sentry environment
from sentry.utils.runner import configure
configure()

# Do something crazy
import sentry
from sentry.models import Team, Project, ProjectKey, User, Organization
from sentry.web.frontend.project_settings import OriginsField
from django.forms import ValidationError
from django.db.utils import IntegrityError

SENTRY_VERSION = tuple(map(lambda x: int(x) if x.isdigit() else x, sentry.get_version().split('.')))


def mark_as_configured():
    sentry.options.set('sentry:version-configured', sentry.get_version())


def create_team(admin_username, team_name, organization_name=None):
    user = User.objects.get(username=admin_username)
    if organization_name is None:
        organization_name = team_name
    org, new_org = Organization.objects.get_or_create(name=organization_name)
    org_member, member_created = org.members.through.objects.get_or_create(organization=org, user=user,
                                                                           defaults={'role': 'owner'})
    team, new = Team.objects.get_or_create(name=team_name,
                                           defaults={'organization': org})
    return team, new


def create_admin(username, email, password):
    try:
        admin = User.objects.create_superuser(username=username, email=email, password=password)
    except IntegrityError:
        print('Superuser "{0}" is already present.'.format(username))
    else:
        print('Superuser "{0}" created successfully.'.format(username))
        return admin
    finally:
        mark_as_configured()


def create_project(team_name, project_name):
    team = Team.objects.get(name=team_name)
    defaults = {'organization': team.organization}
    project, new = Project.objects.get_or_create(name=project_name, team=team,
                                                 defaults=defaults)

    return project, new


def enforce_key(project, key_string):
    key = ProjectKey.objects.get(project=project)
    public, secret = key_string.split(':')
    key.public_key = public
    key.secret_key = secret
    key.save()


def update_origins(team_name, project_name, origins):
    '''
    ``origins`` should be space separated
    '''
    project = Project.objects.get(name=project_name, team__name=team_name)

    # prepare for input
    new_origins = "\n".join(origins.split())
    origins_field = OriginsField()
    try:
        values = origins_field.clean(new_origins)
    except ValidationError as ex:
        print('x ! ' * 50)
        print('Something went wrong while updating allowed domains:')
        print(ex)
        print('x ! ' * 50)
    else:
        project.update_option('sentry:origins', values or [])


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

    to modify allowed domains for a project pass a space separated list like this::

        python create_team_or_project.py origins teamname projectname 'example.com *.example.com'

    to create a superuser::

        python create_team_or_project.py admin username email@foo.bar password
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
    elif command in ('origins',):
        team_name = sys.argv[2]
        project_name = sys.argv[3]
        origins = sys.argv[4]
        update_origins(team_name, project_name, origins)
    elif command in ('admin',):
        username = sys.argv[2]
        email = sys.argv[3]
        password = sys.argv[4]
        create_admin(username, email, password)

if __name__ == '__main__':
    main()
