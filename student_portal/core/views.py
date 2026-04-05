from .forms import StudentForm
from django.shortcuts import render

def home(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            # Later: send to Odoo
            print(name, email)

    else:
        form = StudentForm()

    return render(request, 'home.html', {'form': form})