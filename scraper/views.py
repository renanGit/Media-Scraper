# -*- coding: utf-8 -*-
# Created on Jan 9, 2014
# @author: Renan Santana

from django.shortcuts import render
from django.db import OperationalError
from scraper.models import *
import auxiliary as aux


def welcome(request):
    return render(request, 'welcome.html')


def scrape(title):
    try:
        build = aux.Build()
        build.searchTitle(title)
        details = build.getDetails()
        m = Movie(title=str(details['title']))
        m.save()
        return details['title']

    except aux.FindMovieError as e:
        print e


def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        # elif len(q) > 20:
        #     errors.append('Please enter at most 20 characters.')
        else:
            # for now handle movies with one instance (future: same title differ year)
            try:
                m = Movie.objects.get(title=str(q))  # filter(title=q)
            except OperationalError as e:
                print e
                m = scrape(title=str(q))

            return render(request, 'search_results.html', {'title': m})

    return render(request, 'search_form.html', {'errors': errors})


