from django.shortcuts import render, redirect, get_object_or_404
from .models import CodingContest, LeaderboardEntry
from .forms import CodingContestForm
from django.contrib.auth.decorators import login_required
from .forms import SubmissionForm
@login_required
def contest_list(request):
    contests = CodingContest.objects.all().order_by('-start_time')
    return render(request, 'challenges/contest_list.html', {'contests': contests})

@login_required
def contest_detail(request, pk):
    contest = get_object_or_404(CodingContest, pk=pk)
    leaderboard = LeaderboardEntry.objects.filter(contest=contest).order_by('-score')
    return render(request, 'challenges/contest_detail.html', {
        'contest': contest,
        'leaderboard': leaderboard,
    })
@login_required
def submit_code(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            return redirect('submission_success')  # Create this view or redirect as needed
    else:
        form = SubmissionForm()
    return render(request, 'contests/submit_code.html', {'form': form})

@login_required
def create_contest(request):
    if not request.user.is_faculty:
        return redirect('contest_list')

    if request.method == 'POST':
        form = CodingContestForm(request.POST)
        if form.is_valid():
            contest = form.save(commit=False)
            contest.created_by = request.user
            contest.save()
            return redirect('contest_list')
    else:
        form = CodingContestForm()
    return render(request, 'challenges/create_contest.html', {'form': form})
