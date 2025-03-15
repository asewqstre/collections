from django.shortcuts import render
from django.http import HttpResponseForbidden
from .forms import Create_Collection_Form
from django.contrib.auth.decorators import login_required

@login_required
def create_collection_view(request):
    if request.method == 'POST':
        form = Create_Collection_Form(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            if request.user.collections.filter(name=collection.name).exists(): # Checking if the collection already exists in the logged in user's collections
                return HttpResponseForbidden(f'You already have {collection.name} collection.')
            else:
                collection.user = request.user # Setting the user of collection to the logged in user
                collection.save()
    else:
        form = Create_Collection_Form()
    return render(request, 'collection/create_collection.html', {'form': form})
