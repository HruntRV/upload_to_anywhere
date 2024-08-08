from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View
from .forms import PostForm, CommentForm, SubscribeForm, RegistrationForm, UpdateForm
from .models import Post, Category, Profile, Comment
from django.db.models import Q


def get_categories():
    cats = Category.objects.all()
    count = cats.count()
    half = count // 2
    first_half = cats[:half]
    second_half = cats[half:]
    return {'cats1': first_half, 'cats2': second_half}


def category(request, c=None):
    cObj = get_object_or_404(Category, name=c)
    posts = Post.objects.filter(category=cObj).order_by("-published_date")
    context = {'post_images': posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def index(request):
    posts = Post.objects.all().order_by("-published_date")
    # post_images = Post.objects.filter(title__contains="News")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def post(request, name=None, id=None):
    post = get_object_or_404(Post, title=name, id=id)
    comments = Comment.objects.filter(post=post).order_by('-published_date')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.profile
            comment.save()
            return redirect('post', name=post.title, id=post.id)
    else:
        form = CommentForm()
    context = {
        'post': post,
        'comment': comments,
        'form': form
    }
    context.update(get_categories())
    return render(request, "blog/post.html", context)


def about(request):
    context = {}
    context.update(get_categories())
    return render(request, 'blog/about.html', context)


def services(request):
    context = {}
    context.update(get_categories())
    return render(request, 'blog/services.html', context)


def contact(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts')
    else:
        form = SubscribeForm()

    context = {'form': form}
    context.update(get_categories())
    return render(request, "blog/contact.html", context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    # post_images = Post.objects.all().order_by("-published_date")
    # context = {'post_images': posts}
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = now()
            post.user = request.user
            post.image = form.cleaned_data['image']
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    context = {'form': form}
    context.update(get_categories())
    return render(request, 'blog/create.html', context)


class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


@login_required
def profile(request):
    # profile_data = Profile.objects.get(user=request.id)
    profile_data = get_object_or_404(Profile, user=request.user)
    context = {'profile_data': profile_data}
    context.update(get_categories())
    return render(request, 'blog/profile.html', context)
#
# class MyLoginView(View):
#     def get(self, request):
#         login(request)
#         return redirect('index')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Username']
            first_name = form.cleaned_data['First_name']
            last_name = form.cleaned_data['Last_name']
            gender = form.cleaned_data['Gender']
            email = form.cleaned_data['Mail']
            phone = form.cleaned_data['Phone']
            country = form.cleaned_data['Country']
            city = form.cleaned_data['City']
            password = form.cleaned_data['Password']
            password_confirm = form.cleaned_data['Password_confirm']

            if password == password_confirm:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.first_name = first_name
                new_user.last_name = last_name
                new_user.save()

                new_profile = Profile(user=new_user, gender=gender, phone=phone, country=country, city=city)
                new_profile.save()
                login(request, new_user) # автоматически логинимся

                return redirect('registration_success')
            else:
                form.add_error('Password_confirm', "Passwords do not match")

    else:
        form = RegistrationForm()
    context = {'form': form}
    context.update(get_categories())
    return render(request, "blog/registration.html", context)


def registration_success(request):
    context = {}
    context.update(get_categories())
    return render(request, 'blog/registration_success.html', context)


def update_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()
            profile.gender = form.cleaned_data['Gender']
            profile.phone = form.cleaned_data['Phone']
            profile.country = form.cleaned_data['Country']
            profile.city = form.cleaned_data['City']
            profile.avatar = form.cleaned_data['Avatar']
            profile.save()

            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
                user.save()
                update_session_auth_hash(request, user)

            return redirect('profile')
    else:
        initial_data = {
            'Gender': profile.gender,
            'Phone': profile.phone,
            'Country': profile.country,
            'City': profile.city,
        }
        form = UpdateForm(instance=user, initial=initial_data)

        context = {'form': form}
        context.update(get_categories())
        return render(request, "blog/update_profile.html", context)
