from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

from .models import Article, Profile, UserStatus
from .forms import CustomUserCreationForm, ProfileForm

# Create your views here.

def home(request):
    # Get the latest article (or you can customize as needed)
    article = Article.objects.last()
    return render(request, 'website/home.html', {'article': article})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email address is already registered.')
            else:
                user = form.save(commit=False)
                user.is_active = True  # Activate immediately without email confirmation
                user.save()
                # Don't log in automatically, redirect to login page
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'website/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'website/activation_invalid.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to profile page after login
            try:
                profile = user.profile
                return redirect('profile')
            except Profile.DoesNotExist:
                return redirect('edit_profile')
    else:
        form = AuthenticationForm()
    return render(request, 'website/login.html', {'form': form})

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'website/profile.html', {'profile': profile})

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                image = Image.open(request.FILES['profile_picture'])
                image = image.convert('RGB')
                image.thumbnail((300, 300))  # Resize to max 300x300 preserving aspect ratio

                buffer = BytesIO()
                image.save(buffer, format='JPEG', quality=70)  # Compress image quality to 70%
                image_file = ContentFile(buffer.getvalue())
                profile.profile_picture.save(request.FILES['profile_picture'].name, image_file, save=False)

            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'website/edit_profile.html', {'form': form, 'profile': profile})

@login_required
def admin_panel(request):
    if not request.user.is_staff:
        return redirect('home')

    status_filter = request.GET.get('status', 'all')
    users = User.objects.all()

    if status_filter != 'all':
        user_statuses = UserStatus.objects.filter(status=status_filter).values_list('user', flat=True)
        users = users.filter(id__in=user_statuses)

    user_list = []
    for user in users:
        try:
            user_status = UserStatus.objects.get(user=user)
        except UserStatus.DoesNotExist:
            user_status = UserStatus.objects.create(user=user, status='action')

        user_list.append({
            'user': user,
            'status': user_status,
            'icon': user_status.get_status_icon()
        })

    context = {
        'user_list': user_list,
        'status_filter': status_filter,
        'status_choices': UserStatus.STATUS_CHOICES
    }
    return render(request, 'website/admin_panel.html', context)

@login_required
def user_detail(request, user_id):
    if not request.user.is_staff:
        return redirect('home')

    user = get_object_or_404(User, id=user_id)
    try:
        user_status = UserStatus.objects.get(user=user)
    except UserStatus.DoesNotExist:
        user_status = UserStatus.objects.create(user=user, status='action')

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ['action', 'pending', 'accept', 'reject']:
            user_status.status = action
            user_status.save()
            return redirect('admin_panel')

    context = {
        'user': user,
        'user_status': user_status,
        'profile': profile
    }
    return render(request, 'website/user_detail.html', context)
