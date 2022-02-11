from django.http import HttpResponse
from django.shortcuts import render

def post_list(request):
    http_method = request.method
    my_name = '장고웹프레임워크'
    return HttpResponse('''
        <h2>welcome {name}</h2>
        <p>Http Method : {method}</p>
        <p>Http Encoding : {encoding}</p>
        <p>Http Path : {mypath}</p>
    '''.format(name=my_name
               ,method=http_method
               ,encoding=request.encoding
               ,mypath=request.path
               ))
