from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count, Q
import os
import httpx
from .models import Notification
from django.views.decorators.http import require_http_methods


from .forms import CustomUserCreationForm, DoubtForm, CommentForm
from .models import User, Doubt
from django.http import JsonResponse
from .models import Notification
from django.contrib.auth.decorators import login_required



# ✅ Home
def home(request):
    return render(request, 'forum/home.html')

@login_required
def unread_notification_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})

# ✅ Role-based Dashboard Redirect
@login_required
def dashboard_redirect(request):
    if request.user.role == 'student':
        return redirect('student_dashboard')
    elif request.user.role == 'faculty':
        return redirect('faculty_dashboard')
    else:
        return redirect('home')


# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect('logout_success')

def logout_success(request):
    return render(request, 'forum/logged_out.html')


# ✅ Signup
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.department = form.cleaned_data['department']
            user.year = form.cleaned_data['year']
            user.github_url = form.cleaned_data['github_url']
            if user.role == 'faculty' and user.email.endswith('@mnnit.ac.in'):
                    user.is_verified_faculty = True
                    
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'forum/signup.html', {'form': form})


# ✅ Student Dashboard
@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'student')
def student_dashboard(request):
    doubts = Doubt.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'forum/student_dashboard.html', {'doubts': doubts})


# ✅ Faculty Dashboard
@login_required
@user_passes_test(lambda u: u.is_authenticated and u.role == 'faculty')
def faculty_dashboard(request):
    doubts = Doubt.objects.all().order_by('-created_at')
    return render(request, 'forum/faculty_dashboard.html', {'doubts': doubts})


# ✅ Leaderboard
@login_required
def leaderboard(request):
    top_students = User.objects.filter(role='student').annotate(
        doubts_posted=Count('doubt')
    ).order_by('-doubts_posted')[:10]

    top_faculty = User.objects.filter(role='faculty').annotate(
        verified_count=Count('verified_doubts')
    ).order_by('-verified_count')[:10]

    return render(request, 'forum/leaderboard.html', {
        'top_students': top_students,
        'top_faculty': top_faculty,
    })


# ✅ Ask Doubt (Free AI + Tag + Visibility)
@login_required
def ask_doubt(request):
    if request.method == 'POST':
        form = DoubtForm(request.POST)
        if form.is_valid():
            doubt = form.save(commit=False)
            doubt.student = request.user

            prompt = f"Q: {doubt.title}\n\n{doubt.description}\n\nCode:\n{doubt.code_snippet or ''}"

            try:
                headers = {
                    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                    "Content-Type": "application/json",
                }

                data = {
                    "model": os.getenv("AI_MODEL", "mistralai/mistral-7b-instruct"),
                    "messages": [
                        {"role": "system", "content": "You are a helpful coding assistant."},
                        {"role": "user", "content": prompt},
                    ],
                }

                response = httpx.post("https://openrouter.ai/api/v1/chat/completions",
                                      headers=headers, json=data, timeout=30)

                if response.status_code == 200:
                    doubt.ai_answer = response.json()["choices"][0]["message"]["content"]
                else:
                    doubt.ai_answer = f"⚠️ AI error {response.status_code}: {response.text}"

            except Exception as e:
                doubt.ai_answer = f"⚠️ AI failed:\n{str(e)}"

            doubt.save()
            form.save_m2m()  # Save ManyToMany (tags/categories)
            return redirect('view_doubt', doubt_id=doubt.id)
    else:
        form = DoubtForm()
    return render(request, 'forum/ask_doubt.html', {'form': form})



@login_required
def notifications_view(request):
    notifications = request.user.notifications.order_by('-created_at')
    # Optionally mark them as read
    notifications.update(is_read=True)
    return render(request, 'forum/notifications.html', {'notifications': notifications})

@login_required
def view_doubt(request, doubt_id):
    doubt = get_object_or_404(Doubt, id=doubt_id)

    # Restrict private doubts to owner or faculty
    if not doubt.is_public and doubt.student != request.user and request.user.role != 'faculty':
        return HttpResponseRedirect(reverse('home'))

    comments = doubt.comments.all()
    form = CommentForm()

    # Handle new comment post
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.doubt = doubt
            comment.author = request.user
            comment.save()

            # ✅ Notify student if someone else commented
            if request.user != doubt.student:
                Notification.objects.create(
                    user=doubt.student,
                    message=f'💬 {request.user.username} commented on your doubt "{doubt.title}".'
                )

            return redirect('view_doubt', doubt_id=doubt.id)

    return render(request, 'forum/view_doubt.html', {
        'doubt': doubt,
        'comments': comments,
        'form': form
    })
@login_required
def faculty_profile_by_username(request, username):
    faculty = get_object_or_404(User, username=username, role='faculty')
    doubts = Doubt.objects.filter(verified_by=faculty)
    return render(request, 'forum/faculty_profile.html', {
        'faculty': faculty,
        'verified_doubts': doubts
    })


@login_required
def student_profile(request, username):
    student = get_object_or_404(User, username=username, role='student')
    doubts = Doubt.objects.filter(student=student).order_by('-created_at')
    return render(request, 'forum/student_profile.html', {
        'student': student,
        'doubts': doubts,
    })

# ✅ Faculty Verifies Doubt

@user_passes_test(lambda u: u.is_authenticated and u.role == 'faculty' and u.is_verified_faculty)
@require_http_methods(["GET", "POST"])
def verify_doubt(request, doubt_id):
    doubt = get_object_or_404(Doubt, id=doubt_id)

    if request.method == 'POST':
        suggestion = request.POST.get("faculty_suggestion", "")
        doubt.faculty_verified = True
        doubt.verified_by = request.user
        doubt.faculty_suggestion = suggestion
        doubt.save()
        Notification.objects.create(
            user=doubt.student,
            message=f'✅ Your doubt "{doubt.title}" has been verified by faculty.'
        )

        # ✅ Send notification email to student
        send_mail(
            subject='✅ Your doubt has been verified!',
            message=f'Hi {doubt.student.username},\n\nYour doubt titled "{doubt.title}" has been verified with a suggestion from a faculty member.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[doubt.student.email],
            fail_silently=True
        )
        return redirect('view_doubt', doubt_id=doubt.id)

    return render(request, 'forum/verify_doubt.html', {'doubt': doubt})
