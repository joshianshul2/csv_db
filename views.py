from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
#from .models import Journal, Category
#from .serializers import JournalSerializer
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
#from django.views.generic import ListView
import bcrypt
from .models import User,UserManager,PropertyMaster,Property_TypeMaster,TypeMaster
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
#from .serializers import JournalSerializer
import pandas as pd
import json
import numpy as np
from datetime import datetime
from django.core import mail
from django.template.loader import render_to_string

from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
import functools

def index(request):
    return render(request, 'index2.html')
def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    # hashed_password = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
    # password= User.objects.create()
    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=request.POST['password'], email=request.POST['email'])
    user.save()
    request.session['id'] = user.id
    return redirect('/success')


def disjunction(*conditions):
    return functools.reduce(np.logical_or, conditions)

def Alert(request):
    dfp = pd.read_csv("core/rishu.csv")
    df = pd.read_csv("core/rishuAlert2.csv")
    if request.method == 'GET':
        view_state = request.GET.get('view_state')
        types = request.GET.get('types')
        view_percentage = request.GET.get('view_percentage')
        x = 1 - float(get_float(view_percentage)/100)
        print("Rishuuu",x)
        # akp1 =True
        akp2 = True
        akp3 = True
        print("Available Field",view_state)
        # (1) Condition for State , County and City
        if (view_state and view_percentage) is not None :
            akp1 = compute_county_wise_price(df, dfp, view_state, x);
            # print(df1)
            df1=dfp.loc[akp1, ['lwPropertyId', 'address', 'city', 'state', 'county', 'zip', 'price', 'acres', "Rate", "Url",'types', 'status', 'created_at', 'updated_at']]

        else:
            df1 = dfp

        print("DF1",df1)

        json_records = df1.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_records)
        page = request.GET.get('page', 1)
        paginator = Paginator(data, 500)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages(10))


    return render(request, 'bootstrap_form.html', {'users': users})


def compute_county_wise_price(df1, df2, state, x):
    netprice_per_county = df1[df1['state'] == state]
    netprice_per_county = netprice_per_county.drop('state', axis=1)

    price_per_county = {county: price*x for county, price in netprice_per_county.items()}
    results = []

    for index, row in df2.iterrows():
        if ((row['state'] == state) and (price_per_county[row['county']] > row['Rate'])):
            results.append(True)
        else:
            results.append(False)
    return results

def show(request):
    df = pd.read_csv("core/rishu.csv")
    if request.method == 'GET':
        title_contains_query = request.GET.get('title_contains')
        id_exact_query = request.GET.get('id_exact')
        title_or_author_query = request.GET.get('title_or_author')
        view_count_min = request.GET.get('view_count_min')
        view_count_max = request.GET.get('view_count_max')
        date_min = request.GET.get('date_min')
        date_max = request.GET.get('date_max')
        Udate_min = request.GET.get('date_min2')
        Udate_max = request.GET.get('date_max2')
        view_acres = request.GET.get('view_acres')
        status = request.GET.get('status')
        title2_contains_query = request.GET.get('title2_contains')
        view_state = request.GET.get('view_state')
        types = request.GET.get('types')
        view_percentage = request.GET.get('view_percentage')
        akp1 = df['state']== 'Anji'
        # akp1 =True
        akp2 = True
        akp3 = True
        print("Available Field",title_contains_query)
        # (1) Condition for State , County and City
        if title_contains_query  is not None :
            akp1 = (df['state'] == title_contains_query ) | (df['city'] == title_contains_query) | (df['county'] == title_contains_query)
            # print(df1)
            df1=df.loc[akp1, ['lwPropertyId', 'address', 'city', 'state', 'county', 'zip', 'price', 'acres', "Rate", "Url",'types', 'status', 'created_at', 'updated_at']]

        else:
            df1 =df

        print("DF1",df1)
        # (2) Condition for Types
        if types is not None :
            akp2 = (df1['types'].str.contains(types , na=False))
            # akp2 = (df1['types'] == types)
            df2=df1.loc[akp2, ["lwPropertyId", 'address', 'city', 'state', 'county', 'zip', 'price', 'acres', "Rate", "Url",'types', 'status', 'created_at', 'updated_at']]

        else :
            df2 =df1

        print("DF2",df2)

        # (3) Condition for Status
        if status is not "" :
            print(status)
            akp3 = (df2['status'] == status)
            # akp2 = (df1['status'] == types)
            df3 = df2.loc[akp3, ["lwPropertyId", 'address', 'city', 'state', 'county', 'zip', 'price', 'acres', "Rate", "Url",'types', 'status', 'created_at', 'updated_at']]
        else :
            df3 = df2
        print("DF3",df3)

        # print(view_acres)
        # (4) Condition For Min Price :

        if view_count_min is not None :
            akp4 = df3['price'] >= get_float(view_count_min)
            df4 = df3.loc[akp4, ['lwPropertyId', 'address', 'city', 'state', 'county', 'zip', 'price', 'acres', "Rate", "Url",
                       'types', 'status', 'created_at', 'updated_at']]
        else :
            df4 = df3
        print("DF4",df4)

        # (5) Condition For Max Price :

        if view_count_max  is "100000":
            print("word",view_count_max)
            akp5 = df4['price'] <= get_float(view_count_max)
            df5 = df4.loc[
                akp5, ['lwPropertyId', 'address', 'city', 'state', 'county', 'zip', 'price', 'acres', "Rate", "Url",
                       'types', 'status', 'created_at', 'updated_at']]
        else:
            print("Hello",view_count_max)
            df5 = df4
        print("DF5",df5)

        #(6) Condition for Area :

        if view_acres is not None :
            akp6 = df5['acres'] >= get_float(view_acres)
            df6 = df5.loc[akp6, ['lwPropertyId', 'address', 'city', 'state', 'county', 'zip', 'price', 'acres', "Rate", "Url",
                       'types', 'status', 'created_at', 'updated_at']]
            # print(df5)
        else :
            df6 = df5
        print("DF6",df6)

        # (7) Condition For Publish Date :

        if date_min  is "2000-01-01" and date_max is "2050-01-01":
            print("RishuuuDAte")
            print(date_min)
            print(date_max)
            akp7 = data_within_date(df6, date_min, date_max)
            df7 = df6.loc[akp7, ['lwPropertyId', 'address', 'city', 'state', 'county', 'zip', 'price', 'acres', "Rate", "Url",'types', 'status', 'created_at', 'updated_at']]
        else:
            print("NA Date",date_min)
            df7 = df6
        print("DF7",df7)

        # (7) Condition For Update Date :

        if Udate_min is "2000-01-01" and Udate_max is "2050-01-01":
            akp8 = data_within_date(df7, Udate_min, Udate_max)
            df8 = df7.loc[
                akp8, ['lwPropertyId', 'address', 'city', 'state', 'county', 'zip', 'price', 'acres', "Rate", "Url",
                       'types', 'status', 'created_at', 'updated_at']]
        else:
            print("NA Date", Udate_min)
            df8 = df7
        print("DF8", df8)




        json_records = df7.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_records)
        page = request.GET.get('page', 1)
        paginator = Paginator(data, 5000)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages(10))


    return render(request, 'bootstrap_form.html', {'users': users})

def get_float(s):
    ans_int = 0
    ans_float = 0
    divisor = 1

    int_part = s.split('.')[0]

    for d in int_part:
        ans_int = (ans_int * 10) + int(d)

    if (not s.find('.') == -1):

        float_part = s.split('.')[1]

        for d in float_part:
            ans_float = (ans_float * 10) + int(d)

        divisor = 10 ** len(float_part)

    ans = ans_int + (ans_float / divisor)

    return ans

def data_within_date(df, min_date, max_date):
    created_dates = [date.split()[0] for date in df['created_at']]
    min_d = datetime.strptime(min_date, '%Y-%m-%d')
    max_d = datetime.strptime(max_date, '%Y-%m-%d')
    results = []
    for date in created_dates:
        date = datetime.strptime(date, '%Y-%m-%d')
        if (date >= min_d and date <= max_d):
            results.append(True)
        else:
            results.append(False)
    return results


def login(request):
    print("Rishi")
    rishu = request.POST.get('login_email')
    print("Rishu",rishu)
    if rishu =='purchase@tayloredideas.com':
        print("Login Entry")

        # user = User.objects.get(email__exact='usermail@example.com')
        # if (bcrypt.checkpw(request.POST['login_password'].encode('utf-8'), user.password.encode('utf-8'))):
        if (request.POST.get('login_password') == "usa_texas_property_stuff"):
            print("Sahi Hai")
            # request.session['id'] = user.id
            return redirect('/show')
    return redirect('/')

def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        "user": user
    }
    # job(request)

    return render(request, 'test111.html', context)

def set_password(self, pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    self.password_hash = pwhash.decode('utf8') # decode the hash to prevent is encoded twice


def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request):
    qs = PropertyMaster.objects.all()
    category = PropertyMaster.objects.all()
    title_contains_query = request.GET.get('title_contains')
    id_exact_query = request.GET.get('id_exact')
    title_or_author_query = request.GET.get('title_or_author')
    view_count_min = request.GET.get('view_count_min')
    view_count_max = request.GET.get('view_count_max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    view_acres = request.GET.get('view_acres')
    category = request.GET.get('category')
    reviewed = request.GET.get('reviewed')
    not_reviewed = request.GET.get('notReviewed')

    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(city__icontains=title_contains_query)

    elif is_valid_queryparam(id_exact_query):
        qs = qs.filter(id=id_exact_query)

    elif is_valid_queryparam(title_or_author_query):
        qs = qs.filter(Q(city__icontains=title_or_author_query)).distinct()
                       # | Q(author__name__icontains=title_or_author_query)


    if is_valid_queryparam(view_count_min):
        qs = qs.filter(price__gte=view_count_min)

    if is_valid_queryparam(view_count_max):
        qs = qs.filter(price__lt=view_count_max+"1")

    if is_valid_queryparam(date_min):
        qs = qs.filter(publish_date__gte=date_min)

    if is_valid_queryparam(category) and category != 'Choose...':
        qs = qs.filter(price__name=category)

    if is_valid_queryparam(date_max):
        qs = qs.filter(publish_date__lt=date_max)

    if is_valid_queryparam(view_acres):
        qs = qs.filter(acres__gte=view_acres)
    #
    # if is_valid_queryparam(acres) :
    #     qs = qs.filter(acres__values=acres)

    if reviewed == 'on':
        qs = qs.filter(reviewed=True)

    elif not_reviewed == 'on':
        qs = qs.filter(reviewed=False)

    return qs


def infinite_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    return PropertyMaster.objects.all()[int(offset): int(offset) + int(limit)]


def is_there_more_data(request):
    offset = request.GET.get('offset')
    if int(offset) > PropertyMaster.objects.all().count():
        return False
    return True

# class ReactFilterView(generics.ListAPIView):
#     serializer_class = JournalSerializer
#
#     def get_queryset(self):
#         qs = filter(self.request)
#         return qs


# class ReactInfiniteView(generics.ListAPIView):
#     serializer_class = JournalSerializer
#
#     def get_queryset(self):
#         qs = infinite_filter(self.request)
#         return qs
#
#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=True)
#         return Response({
#             "journals": serializer.data,
#             "has_more": is_there_more_data(request)
#         })



def logout_view(request):
    return render(request,'index2.html')
