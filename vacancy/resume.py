from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse
from django.views import View

from vacancy.forms import ResumeForm
from vacancy.models import Resume


class ResumeLetsStart(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'resume-create.html')


class ResumeView(LoginRequiredMixin, View):

    def get(self, request):
        try:
            resume = get_object_or_404(Resume, user=request.user.id)
        except Http404:
            return redirect(reverse('resume-create'))
        return render(request, 'resume-edit.html', context={'form': ResumeForm(instance=resume)})

    def post(self, request):
        resume = get_object_or_404(Resume, user=request.user.id)
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('resume-edit')
        return render(request, 'resume-edit.html', context={'form': form})


class ResumeNew(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'resume-edit.html', context={'form': ResumeForm})

    def post(self, request):
        form = ResumeForm(request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            return redirect('resume-edit')
        return render(request, 'resume-edit.html', context={'form': form})
