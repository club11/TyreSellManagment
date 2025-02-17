
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
#from . import forms
#from . import models

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import plotly.express as px



class AiarketerTemplateView(TemplateView):
    #model = models.SalesTable
    template_name = 'aimarketer/aimarketer.html'

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)

        fig = px.scatter(x=range(10), y=range(10))
        fig.write_html("aimarketer/aimarketer.html")

        return kwargs