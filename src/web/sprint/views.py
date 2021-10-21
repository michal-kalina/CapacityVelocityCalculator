from django.shortcuts import render

# Create your views here.
def index(request):
    pass


def add(request):
    print("add")
    context = {
        'output': None,
    }
    return render(request, 'sprint/add.html', context)