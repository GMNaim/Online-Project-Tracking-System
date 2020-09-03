from django.shortcuts import render


def dashboard(request):
    return render(request, 'adminusers/dashboard.html')


def client_list(request):
    return render(request, 'adminusers/client_list.html')


def client_add(request):
    return render(request, 'adminusers/client_add.html')


def project_add(request):
    return render(request, 'adminusers/project_add.html')


def project_list(request):
    return render(request, 'adminusers/project_list.html')
