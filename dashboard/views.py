# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from babybuddy.mixins import PermissionRequired403Mixin
from core.models import Child


class Dashboard(LoginRequiredMixin, TemplateView):
    # TODO: Use .card-deck in this template once BS4 is finalized.
    template_name = 'dashboard/dashboard.html'

    # Show the overall dashboard or a child dashboard if one Child instance.
    def get(self, request, *args, **kwargs):
        children = Child.objects.count()
        if children == 0:
            return HttpResponseRedirect(reverse('babybuddy:welcome'))
        elif children == 1:
            return HttpResponseRedirect(
                reverse(
                    'dashboard:dashboard-child',
                    args={Child.objects.first().slug}
                )
            )
        return super(Dashboard, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['objects'] = Child.objects.all().order_by('last_name')
        return context


class ChildDashboard(PermissionRequired403Mixin, DetailView):
    model = Child
    permission_required = ('core.view_child',)
    raise_exception = True
    template_name = 'dashboard/child.html'
