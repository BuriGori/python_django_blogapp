from django.http import HttpResponse
from django.shortcuts import render

from blog.models import Post


def post_list(request):
    # http_method = request.method
    # my_name = '장고웹프레임워크'
    # return HttpResponse('''
    #     <h2>welcome {name}</h2>
    #     <p>Http Method : {method}</p>
    #     <p>Http header : {header}</p>
    #     <p>Http Path : {mypath}</p>
    # '''.format(name=my_name
    #            ,method=http_method
    #            ,header=request.headers['user-agent']
    #            ,mypath=request.path
    #            ))
    from django.utils import timezone
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request,'blog/post_list.html',{'post_list':posts})
