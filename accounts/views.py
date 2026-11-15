from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import role_required
from .models import User
from django.contrib import messages
from .forms import RegisterForm
from .forms import RegisterForm, ProfileForm

@login_required
def dashboard_redirect(request):
    if request.user.role == User.ADMIN:
        return redirect('admin_dashboard')
    return redirect('member_dashboard')

@role_required(User.ADMIN)
def admin_dashboard(request):
    context = {
    'total_users': User.objects.filter(role=User.MEMBER).count(),
    'lenders': User.objects.filter(
        role=User.MEMBER, account_type__in=[User.LENDER, User.BOTH]).count(),
    'borrowers': User.objects.filter(
        role=User.MEMBER, account_type__in=[User.BORROWER, User.BOTH]).count(),
    'recent_users': User.objects.filter(role=User.MEMBER).order_by('-date_joined')[:5],
}
    return render(request, 'dashboards/admin.html', context)

@role_required(User.MEMBER)
def member_dashboard(request):
    return render(request, 'dashboards/member.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
        messages.error(request, 'Please fix the errors below.')
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
        messages.error(request, 'Please fix the errors below.')
    return render(request, 'accounts/profile_edit.html', {'form': form})