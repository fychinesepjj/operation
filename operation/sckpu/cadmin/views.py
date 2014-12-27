from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Home, Project, Team
from django.shortcuts import get_object_or_404


def index(request):
    context = {}
    home = Home.objects.get()
    projects = Project.objects.filter(promote=True).order_by('ordering')
    if projects:
        context.update({'projects': projects})
    if home:
        navlist = home.navlist.all()
        context.update({'home': home, 'navlist': navlist})
    return render_to_response('index.html', context, context_instance=RequestContext(request))


def about(request):
    context = {}
    return render_to_response('about.html', context, context_instance=RequestContext(request))


def project(request):
    context = {}
    projects = Project.objects.order_by('ordering')
    context.update({'projects': projects})
    return render_to_response('project.html', context, context_instance=RequestContext(request))


def project_detail(request, project_id):
    context = {}
    project = get_object_or_404(Project, pk=project_id)
    if project:
        context.update({'project': project})
    return render_to_response('project_detail.html', context, context_instance=RequestContext(request))


def team(request):
    context = {}
    teams = Team.objects.all()
    team_member = []
    for team in teams:
        members = team.members.all()
        team_member.append({'team': team, 'members': members})
    context.update({'team_member': team_member})
    return render_to_response('team.html', context, context_instance=RequestContext(request))


def contact(request):
    context = {}
    return render_to_response('contact.html', context, context_instance=RequestContext(request))
