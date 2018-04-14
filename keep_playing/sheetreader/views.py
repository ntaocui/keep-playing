from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *

def index(request):
	sheet_data = Sheet.objects.all()
	return render(request, 'sheetreader/home.html', {'sheet_data': sheet_data})

def sheetReader(request, pk):
	sheet = get_object_or_404(Sheet, pk=pk)
	return render(request, 'sheetreader/reader.html', {'sheet': sheet})

def newSheet(request):
	form = SheetForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save() # saves the object that was just created
			return HttpResponseRedirect(reverse('sheetreader:index')) # once completed, return to home
	return render(request, "sheetreader/sheet_form.html", {'form': form})

def updateSheet(request, pk=None):
	instance = get_object_or_404(Sheet, pk=pk)
	form = SheetForm(request.POST or None, request.FILES or None, instance=instance)
	# if form submission was successful
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('sheetreader:index'))
	return render(request, "sheetreader/sheet_form.html", {'form': form})

def deleteSheets(request):
	items = request.POST.getlist('items') # receives a list of the items through a request.POST
	Sheet.objects.filter(id__in=request.POST.getlist('items')).delete()
	return HttpResponseRedirect(reverse('sheetreader:index'))