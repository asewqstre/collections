from django.shortcuts import render
from django.http import HttpResponseForbidden
from .forms import Create_Collection_Form
from django.contrib.auth.decorators import login_required
from .models import Collection, Word

def save_words(request, collection):
    """
    Provide request and collection as parameters when using in views.
    This function saves words from the form input named words to the collection.
    """
    if request.method == 'POST':
        words = request.POST.get('words') # Get the words from the form
        if words:
            words = words.split(',') # Split the words by comma and create Word objects for each word removing leading/trailing spaces
            for word in words:
                word = word.lower() # Convert the word to lowercase
                word = word.strip() # Remove leading/trailing spaces
                if not Word.objects.filter(word=word).exists(): # Check if the word already exists in the database
                    # Create a new Word object if it doesn't exist
                    new_word = Word.objects.create(word=word) # Create a new Word object and add it to the collection
                    new_word.save()
                    collection.words.add(new_word) # Create a many-to-many relationship between the collection and the new word
                else:
                    existing_word = Word.objects.get(word=word) # Get the existing word from the database
                    collection.words.add(existing_word) # Create a many-to-many relationship between the collection and the existing word

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
            
            save_words(request, collection) # Save the words to the collection
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
