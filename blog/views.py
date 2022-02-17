from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.forms import PostModelForm, PostForm, Comment, CommentModelForm
from blog.models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


#Views에는 항상 request가 있어야함

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


def post_list(request):
    post_querysset=Post.objects.filter(published_date__lte=timezone.now())
    paginator = Paginator(post_querysset,2)

    try:
        page_number = request.GET.get('page')
        page =paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'post_list': page})



def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = CommentModelForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('post_detail', pk=post.pk)
    else:
        form = CommentModelForm
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def post_remove(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('post_list_home')


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'postform': form})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            clean_data_dict = form.cleaned_data
            post = Post.objects.create(
                author=request.user,
                title=clean_data_dict.get('title'),
                text=clean_data_dict.get('text'),
                published_date=timezone.now()
            )
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'postform': form})


def post_new_modelform(request):
    if request.method == 'POST':
        post_form = PostModelForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        post_form = PostModelForm()
    return render(request, 'blog/post_edit.html', {'form': post_form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_list_home(request):
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
    return render(request, 'blog/post_list.html', {'post_list': posts})
