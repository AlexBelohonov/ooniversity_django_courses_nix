from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentModelForm
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import logging
logger = logging.getLogger(__name__)


# Create your views here.
class StudentDetailView(DetailView):
    model = Student

    logger.debug('Students detail view has been debugged!')
    logger.warning('Logger of students detail view warns you!')
    logger.info('Logger of students detail view informs you!')
    logger.error('Students detail view went wrong!')


class StudentListView(ListView):
    model = Student
    paginate_by = 2
    queryset = Student.objects.order_by('id')

    def get_queryset(self):
        qs = super().get_queryset()
        self.course_id = self.request.GET.get('course_id', None)

        if self.course_id:
            qs = qs.filter(courses__id=self.course_id)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.course_id:
            context['course_id_get'] = self.course_id

        return context


class StudentCreateView(CreateView):
    model = Student
    success_url = reverse_lazy('students:list_view')
    #form_class = StudentModelForm
    fields = '__all__'

    def form_valid(self, form):
        response = super().form_valid(form)
        full_name = self.object.name + ' ' + self.object.surname
        messages.success(self.request, 'Student ' + full_name +  ' has been successfully added.')

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Student registration'

        return context


class StudentUpdateView(UpdateView):
    model = Student
    success_url = reverse_lazy('students:list_view')
    form_class = StudentModelForm
    #fields = '__all__'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Info on the student has been successfully changed.')

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Student info update'

        return context


class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('students:list_view')
    form_class = StudentModelForm
    #fields = '__all__'

    def delete(self, request, *args, **kwargs):
        response = super().delete(self, request, *args, **kwargs)
        full_name = self.object.name + ' ' + self.object.surname
        messages.success(self.request, 'Info on ' + full_name + ' has been successfully deleted.')

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Student info suppression'

        return context