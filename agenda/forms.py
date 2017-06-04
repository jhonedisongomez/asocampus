# -*- coding: utf-8 -*-
from django import forms
from .models import ActivityRoom
from  rooms.models import Room

from .models import TopicAgenda, Agenda


class CreateAgendaForm(forms.ModelForm):

    activity_rooms = forms.ModelChoiceField(queryset=ActivityRoom.objects.filter(active=True),empty_label="por favor seleccione una opcion",widget=forms.Select(attrs={'class':'form-control'}))
    agendas = forms.ModelChoiceField(queryset=Agenda.objects.filter(active=True).order_by('pk'),empty_label="por favor seleccione una opcion",widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Agenda
        fields = '__all__'
