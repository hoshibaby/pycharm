from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from posts.forms import PostCreateForm, PostUpdateForm
from posts.models import Post


# Create your views here.
def create_post(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.save()
            messages.success(request,'게시글 등록')
            return redirect("posts:list")
        else:
            messages.error(request,'게시글 등록 실패')
    return  render(request, 'posts/create.html', {'form': form})
    # return HttpResponse('게시글 등록')
def get_post(request, post_id):
    # post = Post.objects.get(id=post_id)
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/read.html', {'post': post})
    # return HttpResponse('게시글 보기')

def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostUpdateForm(instance=post)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, '게시글 수정')
            return redirect("posts:read", post_id=post.id)
        else:
            messages.error(request, "비밀번호 불일치")
    return render(request, 'posts/update.html',{'form': form})
    # return HttpResponse('게시글 수정')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    password = request.POST.get('password')

    if request.method == 'POST':
        if password == post.password:
            post.delete()
            messages.success(request, '게시글 삭제')
            return redirect("posts:list")
        else:
            messages.error(request,"비밀번호 불일치")
            return redirect("posts:read",post_id=post.id)
    # return HttpResponse('게시글 삭제')
def get_posts(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'posts/list.html', {'posts': posts})
    # return HttpResponse('게시글 목록')