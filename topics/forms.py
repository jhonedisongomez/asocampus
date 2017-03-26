# -*- coding: utf-8 -*-
from django import forms
from .models import ActivityRoom
from  rooms.models import Room
from activities.models import Activities
from .models import Topic


class CreateActivityRoomForm(forms.ModelForm):

    rooms = forms.ModelChoiceField(queryset=Room.objects.filter(active=True).order_by('room_name'),empty_label="por favor seleccione una opcion",widget=forms.Select(attrs={'class':'form-control'}))
    activities = forms.ModelChoiceField(queryset=Activities.objects.filter(active=True).order_by('thopic'),empty_label="por favor seleccione una opcion",widget=forms.Select(attrs={'class':'form-control'}))
    topics = forms.ModelChoiceField(queryset=Topic.objects.filter(active=True).order_by('topic_name'),empty_label="por favor seleccione una opcion",widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Room
        fields = '__all__'
