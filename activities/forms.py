# -*- coding: utf-8 -*-
from django import forms
from .models import Activities
from country.models import *

class VerifySignUpForm(forms.ModelForm):

    #activities = forms.ModelChoiceField(queryset=Activities.objects.filter(active=True),empty_label="por favor seleccione una opcion",widget=forms.Select(attrs={'class':'form-control isSelected'}))

    #obj_municipio = SectionType.objects.filter(section_type_name = 'Municipio',active = True)
    #section_type_code = obj_municipio[0].section_type_code

   # municipios = forms.ModelChoiceField(queryset=Section.objects.filter(active=True,fk_section_type_code = section_type_code),empty_label="por favor seleccione una opcion",widget=forms.Select(attrs={'class':'form-control isSelected', 'onchange':'loadRoom()'}))


    class Meta:
        model = Activities
        fields = '__all__'
