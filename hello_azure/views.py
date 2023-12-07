import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import csv
from django.http import HttpResponse
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import pandas as pd

def index(request):
    print('Request for index page received')
    return render(request, 'hello_azure/index.html')


@csrf_exempt
def hello(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            print("Request for hello page received with name=%s" % name)
            context = {'name': name}
            return render(request, 'hello_azure/hello.html', context)
    else:
        return redirect('index')


def name(request):
    print('Request for name page received')
    return render(request, 'hello_azure/name.html')


def show_reviews(request):
    reviews_df = pd.read_csv('amazon-reviews.csv')
    cities_df = pd.read_csv('us-cities.csv')

    all_reviews = []
    for index, row in reviews_df.iterrows():
        city_details = cities_df[cities_df['city'] == row['city']].iloc[0]
        all_reviews.append({
            'score': row['score'],
            'title': row['title'],
            'review': row['review'],
            'city':row['city'],
            'city_link': f'#',
            'city_details': f'City: {city_details["city"]}<br>Latitude: {city_details["lat"]}<br>Longitude: {city_details["lng"]}<br>Country: {city_details["country"]}<br>State: {city_details["state"]}<br>Population: {city_details["population"]}',
            'image_path': f'static/images/score-{row["score"]}.jpg'
        })

        # 分页
        page = request.GET.get('page', 1)

        try:
            page = int(page)
            page = max(1, page)  # 确保页码不小于1
        except ValueError:
            page = 1

        paginator = Paginator(all_reviews, 10)  # 每页显示10条数据
        try:
            reviews = paginator.page(page)
        except PageNotAnInteger:
            reviews = paginator.page(1)
        except EmptyPage:
            reviews = paginator.page(paginator.num_pages)

    return render(request, 'hello_azure/reviews.html', {'reviews': reviews})

