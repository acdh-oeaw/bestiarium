from django.shortcuts import render

# Create your views here.


def chapters(request):
    template_name = 'omens/index.html'
    return render(request, template_name, context)


def omen(request, omenname):
    pass
