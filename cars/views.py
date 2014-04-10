from sys import stdout
from django.shortcuts import render
from django.http import HttpResponse
from .models import CarMarks, CarSeries, CarModels
from django.views.generic import View,ListView,DetailView,TemplateView, CreateView,FormView
from .parser_utils import get_all_prices_per_page_usd, AutoRiaDict, get_auto_ria_info
from .forms import SearchForm, CarSeriesForm
import logging
from sys import stdout
import pdb


# Create your views here.


class CarMarksView(FormView):
    template_name = "cars/car-marks-view.html"
    form_class = CarSeriesForm


class SearchView(FormView):
    model = CarMarks
    template_name = 'cars/search-view.html'
    form_class = SearchForm


    def get_object(self):
        return CarMarks.objects.get(pk=int(self.request.GET.get("car_mark")))


    def get_form(self, form_class):
        return form_class(instance = self.get_object())


    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        if self.request.GET.get("series"):
            p = AutoRiaDict()
            mark = CarMarks.objects.get(pk=int(self.request.GET.get("car_mark")))
            series = CarSeries.objects.get(pk=int(self.request.GET.get("series")))
            p["marka"]= str(mark.auto_ria_id)
            p["model"]= series.series_auto_ria_id
            lst = get_auto_ria_info(p)
            context["mark"] =  mark.name
            context["series"] = series.name
            context["search_results"] = lst
            context["series_id"] = series.id
        return context








# class SkodaView(ListView):
#     queryset = CarSeries.objects.filter(car_mark__name = 'Skoda')
#     template_name = 'cars/skoda-view.html'
#
#
# class SearchView(FormView):
#     template_name = 'cars/search-view.html'
#     form_class = SearchForm
#
#
#     def get_object(self):
#         obj = CarSeries.objects.get(pk=int(self.kwargs.get("series_id")))
#         return obj
#
#     def get_form(self, form_class):
#         series = self.get_object()
#         return form_class(initial = {'name':series.name})
#
#
#     def get_context_data(self, **kwargs):
#         p = AutoRiaDict()
#         mark = CarMarks.objects.get(pk=int(self.kwargs.get("mark_id")))
#         series = CarSeries.objects.get(pk=int(self.kwargs.get("series_id")))
#         p["marka"]= str(mark.auto_ria_id)
#         p["model"]= series.series_auto_ria_id
#         # lst = get_all_prices_per_page_usd(p)
#         context = super(SearchView, self).get_context_data(**kwargs)
#         context["mark"] =  mark.name
#         context["series"] = series.name
#         # context["prices"] = lst
#         return context
#
# class AllMarkView(ListView):
#     template_name = 'cars/skoda-view.html'
#
#     def get_queryset(self):
#         return CarSeries.objects.filter(car_mark__name = self.args[0])
#
#









