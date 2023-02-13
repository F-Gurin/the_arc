from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings

from .forms import SessionsForm
from .models import Sessions, Patient, Psychologist

def index(request):
    template = 'web_admin/index.html'
    context = {}
    return render(request, template, context)


@login_required
def sessions_list(request):
    template = 'web_admin/sessions_list.html'
    sessions = Sessions.objects.filter(psychologists=request.user, date_time__gte=datetime.now())
    paginator = Paginator(sessions, settings.NUMBER_OF_SESSIONS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def session_detail(request, session_id):
    template = 'web_admin/session_detail.html'
    session = get_object_or_404(Sessions, id=session_id)
    context = {
        'session': session,
    }
    return render(request, template, context)


@login_required
def patient(request, patient_id):
    template = 'web_admin/profile.html'
    patient = get_object_or_404(Patient, id=patient_id)
    context = {
        'patient': patient,
    }
    return render(request, template, context)


@login_required
def session_create(request):
    template = 'web_admin/create.html'
    form = SessionsForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        create_session = form.save(commit=False)
        psychologist = get_object_or_404(Psychologist, username=request.user)
        create_session.psychologists = psychologist
        create_session.save()
        return redirect('web_admin:sessions_list')
    context = {'form': form}
    return render(request, template, context)

@login_required
def session_edit(request, session_id):
    template = 'web_admin/create.html'
    session = get_object_or_404(Sessions, id=session_id)
    if request.user != session.psychologists:
        return redirect('web_admin:session_detail', session_id)
    form = SessionsForm(
        request.POST or None,
        instance=session,
        files=request.FILES or None,
    )

    if form.is_valid():
        form.save()
        return redirect('web_admin:session_detail', session_id)

    context = {'form': form, 'session': session, 'is_edit': True}
    return render(request, template, context)
