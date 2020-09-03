from django.shortcuts import render


def base(request):
    return render(request, 'base/base_template.html')
