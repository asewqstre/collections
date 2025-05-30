from django.shortcuts import render
from django.http import HttpResponseForbidden
from .forms import Create_Collection_Form
from django.contrib.auth.decorators import login_required
from .models import Collection

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

@login_required
def delete_collection_view(request, pk):
    collection = Collection.objects.get(pk=pk)
    if not Collection.objects.filter(user=request.user).exists(): # Checking if the collection belongs to the logged in user
        # If the collection does not belong to the user, return a forbidden response
        return HttpResponseForbidden('You are not allowed to delete this collection.')
    if request.method == 'POST': # Deleting the collection if form is submitted
        collection.delete()
    return render(request, 'collection/delete_collection.html', {'collection': collection})

@login_required
def update_collection_view(request, pk):
    collection = Collection.objects.get(pk=pk)
    if not Collection.objects.filter(user=request.user).exists(): # Checking if the collection belongs to the logged in user
        # If the collection does not belong to the user, return a forbidden response
        return HttpResponseForbidden('You are not allowed to update this collection.')
    if request.method == 'POST':
        form = Create_Collection_Form(request.POST, instance=collection)
        if form.is_valid():
            if request.user.collections.filter(name=collection.name).exclude(pk=pk).exists(): # Checking if the collection already exists in the logged in user's collections
                return HttpResponseForbidden(f'You already have {collection.name} collection.')
            collection.user = request.user # Resetting the user of collection to the logged in user because user field is empty while updating the collection
            form.save()
    else:
        form = Create_Collection_Form(instance=collection)  # Pre-fill the form with the existing collection data
    return render(request, 'collection/update_collection.html', {'form': form, 'collection': collection})
