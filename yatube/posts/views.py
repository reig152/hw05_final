from django.shortcuts import get_object_or_404
from .models import Post, Group, User, Comment, Follow
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

POSTS_AMOUNT = 10


class Index(generic.ListView):
    """ListView главной страницы"""
    model = Post
    template_name = 'posts/index.html'
    paginate_by = POSTS_AMOUNT
    context_object_name = 'posts'


class GroupPostsView(generic.ListView):
    """Рефакторинг страницы группы"""
    template_name = 'posts/group_list.html'
    paginate_by = POSTS_AMOUNT

    def get_queryset(self):
        self.group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return Post.objects.filter(group=self.group)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.group
        return context


class UserPostsView(generic.ListView):
    """Рефакторинг страницы пользователя"""
    template_name = 'posts/profile.html'
    paginate_by = POSTS_AMOUNT

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.author.posts.all()
        context['posts_number'] = posts.count()
        context['author'] = self.author
        if self.request.user.is_authenticated:
            context['following'] = Follow.objects.filter(
                user=self.request.user, author=self.author
            )
        return context


class PostDisplay(generic.DetailView):
    """Рефакторинг, отображает детали поста и форму для комментариев"""
    model = Post
    context_object_name = 'post'
    template_name = 'posts/post_detail.html'

    def get_object(self):
        self.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return self.post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.post.text[:30]
        context['comments'] = Comment.objects.filter(post=self.post)
        context['posts_number'] = Post.objects.filter(
            author=self.post.author).count()
        context['form'] = CommentForm()
        return context


class PostComments(LoginRequiredMixin, generic.CreateView):
    """Рефакторинг, отвечает за добавление комментариев"""
    model = Post
    form_class = CommentForm
    template_name = 'posts/post_detail.html'

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_object()
        return super().form_valid(form)

    def get_success_url(self):
        self.obj = self.get_object()
        return reverse_lazy('posts:post_detail', kwargs={
            'post_id': self.obj.pk})


class PostDetail(generic.View):
    """Определяет запрос, перенаправляет на соответствующую функцию"""
    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComments.as_view()
        return view(request, *args, **kwargs)


class PostCreate(LoginRequiredMixin, generic.CreateView):
    """Рефакторинг - создание поста"""
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts:profile', kwargs={
            'username': self.request.user})


class PostEdit(LoginRequiredMixin, generic.UpdateView):
    """Рефакторинг - редактирование поста"""
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def get_object(self):
        self.postt = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return self.postt

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        self.obj = self.get_object()
        return reverse_lazy('posts:post_detail', kwargs={
            'post_id': self.obj.pk})


class FollowIndex(LoginRequiredMixin, generic.ListView):
    """Вывод постов авторов, на которых подписан пользователь"""
    template_name = 'posts/follow.html'
    paginate_by = POSTS_AMOUNT
    context_object_name = 'posts'

    def get_queryset(self):
        self.follower = get_object_or_404(User, username=self.request.user)
        self.author = Follow.objects.filter(user=self.follower).values_list(
            'author',
            flat=True,
        )
        self.posts = Post.objects.filter(author__in=self.author)
        return self.posts


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    is_follower = Follow.objects.filter(user=user, author=author)
    if user != author and not is_follower.exists():
        Follow.objects.create(user=user, author=author)
    return redirect('posts:follow_index')


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=user, author=author).delete()
    return redirect('posts:follow_index')
