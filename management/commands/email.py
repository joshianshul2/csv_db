import datetime
import random
from django.core.management.base import BaseCommand
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Sum, Avg
from core.models import User, UserManager, PropertyMaster, Property_TypeMaster, TypeMaster, AvgMaster
import requests

from django.core import mail
from django.template.loader import render_to_string

from django.utils.html import strip_tags
from django.db.models import F

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.E_mail()

    def E_mail(self) :
        print("RAm Sharma")

            # for i in akp:
            #     print(i['state'])
        r=AvgMaster.objects.all().values()
        print(r)
        print("Hero")
        akp = AvgMaster.objects.filter(Rate__gte=F('FinaleValue')).values()
        print(akp)
        subject = 'Anshul'
        context = {
                        'aj': akp,
                        }
        html_message = render_to_string('bootstrap_form.html',context)
        plain_message = strip_tags(html_message)
        from_email = 'joshi.anshul2@gmail.com'
        to = 'jtaylor@tayloredideas.com'

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return True
