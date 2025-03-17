from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def test(request):
  header = request.headers
  params = request.GET
  param = request.GET.get('kaka')
  post_data = request.body
  print("~~~~~~~~~")
  print(header)
  print("~~~~~~~~~")
  print(params)
  print("~~~~~~~~~")
  print(param)
  print("~~~~~~~~~")
  print(post_data)
  print("~~~~~~~~~")
  data = json.loads(post_data)
  print(data)
  
  return JsonResponse(data)