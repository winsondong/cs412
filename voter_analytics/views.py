"""
File: voter_analytics/views.py
Author: Winson Dong (winson@bu.edu)
Description:
    - VoterListView: paginated voter table with filters.
    - VoterDetailView: detailed info for a single voter.
    - GraphListView: displays interactive Plotly graphs of voter data.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import datetime

import plotly
import plotly.graph_objs as go


# Create your views here.
class VoterListView(ListView):
    ''' View to display voters '''
    model = Voter
    template_name = 'voter_analytics/results.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_year = datetime.datetime.now().year
        birth_years = range(current_year - 100, current_year - 17)

        context["birth_years"] = birth_years
        return context


    def get_queryset(self):
        result = super().get_queryset()

        if self.request.GET:
            party = self.request.GET.get('party')
            min_birth_year = self.request.GET.get('min_birth_year')
            max_birth_year = self.request.GET.get('max_birth_year')
            voter_score = self.request.GET.get('voter_score')
            v20state = self.request.GET.get('v20state')
            v21town = self.request.GET.get('v21town')
            v21primary = self.request.GET.get('v21primary')
            v22general = self.request.GET.get('v22general')
            v23town = self.request.GET.get('v23town')

            query = Voter.objects.all()

            if party:
                query = query.filter(party_affiliation=party)
            if min_birth_year:
                query = query.filter(dob__year__gte=min_birth_year)
            if max_birth_year:
                query = query.filter(dob__year__lte=max_birth_year)
            if voter_score:
                query = query.filter(voter_score=voter_score)
            if v20state:
                query = query.filter(v20state=True)
            if v21town:
                query = query.filter(v21town=True)
            if v21primary:
                query = query.filter(v21primary=True)
            if v22general:
                query = query.filter(v22general=True)
            if v23town:
                query = query.filter(v23town=True)

            result = query

        return result
    
class VoterDetailView(DetailView):
    ''' View to display a single voter '''

    model = Voter
    template_name = "voter_analytics/voter.html"
    context_object_name = 'voter'


class GraphListView(ListView):
    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"

    def get_queryset(self):
        
        result = super().get_queryset()

        if self.request.GET:
            party = self.request.GET.get('party')
            min_birth_year = self.request.GET.get('min_birth_year')
            max_birth_year = self.request.GET.get('max_birth_year')
            voter_score = self.request.GET.get('voter_score')
            v20state = self.request.GET.get('v20state')
            v21town = self.request.GET.get('v21town')
            v21primary = self.request.GET.get('v21primary')
            v22general = self.request.GET.get('v22general')
            v23town = self.request.GET.get('v23town')

            query = Voter.objects.all()

            if party:
                query = query.filter(party_affiliation=party)
            if min_birth_year:
                query = query.filter(dob__year__gte=min_birth_year)
            if max_birth_year:
                query = query.filter(dob__year__lte=max_birth_year)
            if voter_score:
                query = query.filter(voter_score=voter_score)
            if v20state:
                query = query.filter(v20state=True)
            if v21town:
                query = query.filter(v21town=True)
            if v21primary:
                query = query.filter(v21primary=True)
            if v22general:
                query = query.filter(v22general=True)
            if v23town:
                query = query.filter(v23town=True)

            result = query

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = context['voters']
        num_voters = len(voters)

        current_year = datetime.datetime.now().year
        birth_years = range(current_year - 100, current_year - 17)
        context["birth_years"] = birth_years

        # Graph 1: Voter Birth Year Distribution
        birth_year_counts = {}
        for v in voters:
            if v.dob:
                year = v.dob.year
                birth_year_counts[year] = birth_year_counts.get(year, 0) + 1

        birth_years = sorted(birth_year_counts)
        birth_counts = [birth_year_counts[year] for year in birth_years]

        fig1 = go.Figure(
            data=[go.Bar(x=birth_years, y=birth_counts)],
            layout=go.Layout(
                title=f'Voter Birth Year Distribution (n={num_voters})',
                xaxis_title='Birth Year',
                yaxis_title='Number of Voters'
            )
        )
        bar_div = plotly.offline.plot(
                    fig1,
                    auto_open=False,
                    output_type='div'
                )

        context['bar_div'] = bar_div

        # Graph 2: Party Affiliation Pie Chart
        party_counts = {}
        for v in voters:
            party = v.party_affiliation
            party_counts[party] = party_counts.get(party, 0) + 1

        party_labels = sorted(party_counts)
        party_values = [party_counts[party] for party in party_labels]

        fig2 = go.Figure(
            data=[go.Pie(labels=party_labels, values=party_values)],
            layout=go.Layout(
                title=f'Voter Distribution by Party (n={num_voters})'
            )
        )

        pie_div = plotly.offline.plot(
                    fig2,
                    auto_open=False,
                    output_type='div'
                )
        context['pie_div'] = pie_div

        # Graph 3: Election Participation Bar Chart
        election_labels = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = {label: 0 for label in election_labels}

        for v in voters:
            if v.v20state:
                election_counts['v20state'] += 1
            if v.v21town:
                election_counts['v21town'] += 1
            if v.v21primary:
                election_counts['v21primary'] += 1
            if v.v22general:
                election_counts['v22general'] += 1
            if v.v23town:
                election_counts['v23town'] += 1

        x_elections = election_labels
        y_counts = [election_counts[label] for label in x_elections]

        fig3 = go.Figure(
            data=[go.Bar(x=x_elections, y=y_counts)],
            layout=go.Layout(
                title=f'Voter Count by Election (n={num_voters})',
                xaxis_title='Election',
                yaxis_title='Number of Voters'
            )
        )

        election_bar_div = plotly.offline.plot(
                    fig3,
                    auto_open=False,
                    output_type='div'
                )
        context['election_bar_div'] = election_bar_div

        return context




