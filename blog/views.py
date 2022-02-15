from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.forms import PostModelForm
from blog.models import Post


def post_new(request):
    if request.method=='POST':
        post_form = PostModelForm(request.POST)
        if post_form.is_valid():
            post = form = post_form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        post = PostModelForm()
    return render(request, 'blog/post_edit.html', {'form': post})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

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
