# -*- coding: utf-8 -*-
from django import forms
from country.models import section, sectionType

class ListMunicipio(forms.ModelForm):

    #obj_section_type = ""
    obj_section_type = sectionType.objects.filter(section_type_name = "Municipio", active = True)
    """if obj_section_type:

        section_type_code = obj_section_type[0].section_type_code
    else:

        section_type_code = "" """
    section_type_code = obj_section_type[0].section_type_code
    municipios = forms.ModelChoiceField(queryset=section.objects.filter(active=True, fk_section_type_code = section_type_code).order_by('section_name'),empty_label="por favor seleccione una opcion",widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = sectionType
        fields = '__all__'
