from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request, 'cs/cs.html')

def review_report(request):
    return render(request, 'reviews/report_list.html')