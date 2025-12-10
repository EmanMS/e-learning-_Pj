# courses/decorators.py
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # تحقق من صلاحية الادمن
        if not (request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == 'admin')):
            return HttpResponseForbidden("You don't have permission to access the admin dashboard")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def instructor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # السماح للإدمن والمدرسين
        if not ((hasattr(request.user, 'is_instructor') and request.user.is_instructor) or 
                (hasattr(request.user, 'is_admin') and request.user.is_admin) or 
                request.user.is_superuser):
            return HttpResponseForbidden("You don't have permission to access instructor features")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view