from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from cabot.cabotapp.models import StatusCheck
from cabot.cabotapp.views import (CheckCreateView, CheckUpdateView,
                                  StatusCheckForm, base_widgets)

from .models import PrometheusStatusCheck


class PrometheusStatusCheckForm(StatusCheckForm):
    symmetrical_fields = ('service_set', 'instance_set')

    class Meta:
        model = PrometheusStatusCheck
        fields = (
            'name',
            'host',
            'port',
            'query',
            'timeout',
            'frequency'
        )

        widgets = dict(**base_widgets)
        widgets.update({
            'host': forms.TextInput(attrs={
                'style': 'width: 100%',
                'placeholder': 'service.arachnys.com',
            })
        })


class PrometheusCheckCreateView(CheckCreateView):
    model = PrometheusStatusCheck
    form_class = PrometheusStatusCheckForm


class PrometheusCheckUpdateView(CheckUpdateView):
    model = PrometheusStatusCheck
    form_class = PrometheusStatusCheckForm


def duplicate_check(request, pk):
    pc = StatusCheck.objects.get(pk=pk)
    npk = pc.duplicate()
    return HttpResponseRedirect(reverse('update-prometheus-check', kwargs={'pk': npk}))