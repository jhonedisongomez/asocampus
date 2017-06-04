# -*- coding: utf-8 -*-
from django import forms
from activities.models import *

class VerifySignUpForm(forms.ModelForm):

    activities = forms.ModelChoiceField(queryset=Activities.objects.filter(active=True, isPaid = True),empty_label="por favor seleccione una opcion",widget=forms.Select(attrs={'class':'form-control  isSelected'}))

    class Meta:
        model = Activities
        fields = '__all__'
