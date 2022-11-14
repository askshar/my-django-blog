from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Comment
from .forms import CommentForm

# Create your views here.

"""
@login_required(login_url='login')
def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)
    
"""


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_comments = post.post_comment.all().order_by('-pub_date')
    comments_count = post.post_comment.all().count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
        'post_comments': post_comments,
        'comments_count': comments_count
    }
    return render(request, 'blog/post_detail.html', context)


def update_comment(request, comment_id, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)
    form = CommentForm(instance=comment)

    if comment.user == request.user:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
            return redirect(f'/post/{post_id}')
    else:
        return HttpResponse("Unauthorized request.")
    context = {
        'form': form
    }

    return render(request, 'blog/update-comment.html', context)


def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user == request.user:
        if request.method == 'POST':
            comment.delete()
            return redirect(f'/post/{post_id}')
    else:
        return HttpResponse("Unauthorized request.")

    context = {"post": post, "comment": comment}

    return render(request, 'blog/delete_comment.html', context)

