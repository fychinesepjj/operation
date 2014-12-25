from django.shortcuts import render_to_response


def index(request):
    context = {}
    return render_to_response('index.html', context)


def about(request):
    context = {}
    return render_to_response('about.html', context)


def project(request):
    context = {}
    return render_to_response('project.html', context)


def team(request):
    context = {}
    return render_to_response('team.html', context)


def contact(request):
    context = {}
    return render_to_response('contact.html', context)
