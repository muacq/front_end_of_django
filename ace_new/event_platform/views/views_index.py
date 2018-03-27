from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def explore(request):
    return render(request, "explore.html")


def question_detail(request):
    return render(request, "question_detail.html")