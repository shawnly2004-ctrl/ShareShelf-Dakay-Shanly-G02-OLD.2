from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import role_required
from .models import User

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