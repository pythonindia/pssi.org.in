# -*- coding: utf-8 -*-
import json
import hashlib, pickle

from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site

from .models import Nomination, NominationType, VotingURL, UserVoting
from .forms import NominationForm
from common import emailer
from board.models import BoardMember
from apps.common.emailer import send_voting_email
# from django.contrib.sites.models import Sites


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request,  *args, **kwargs)


def is_board_member(user):
    if BoardMember.objects.filter(user=user).exists():
        return True
    return False


class NominationTypeListView(ListView, LoginRequiredMixin):
    model = NominationType
    template_name = 'nominations/list.html'
    context_object_name = 'nomination_type_list'

    def get_context_data(self, *args, **kwargs):
        context = super(
            NominationTypeListView, self).get_context_data(*args, **kwargs)
        context['nomination_type_list'] = NominationType.objects.filter(
            active=True).order_by('id')
        context['board_member'] = is_board_member(self.request.user)
        return context


class NomineeListView(ListView, LoginRequiredMixin):
    model = NominationType
    template_name = 'nominations/nominee_list.html'
    context_object_name = 'nomination_type_list'

    def dispatch(self, request, *args, **kwargs):
        if not is_board_member(self.request.user):
            return HttpResponseForbidden("Not board Member")
        return super(NomineeListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(
            NomineeListView, self).get_context_data(*args, **kwargs)
        nomination_type = get_object_or_404(
            NominationType, slug=self.kwargs.get('slug'), active=True)
        context['nomination_list'] = Nomination.objects.filter(
            ntype=nomination_type)
        return context


class NominationCreateView(CreateView, LoginRequiredMixin):
    model = Nomination
    form_class = NominationForm
    template_name = 'nominations/nominations.html'
    success_url = reverse_lazy('nominee_req_success')

    def get_context_data(self, *args, **kwargs):
        context = super(
            NominationCreateView, self).get_context_data(*args, **kwargs)
        context['ntype'] = get_object_or_404(
            NominationType, slug=self.kwargs.get('slug'), active=True)
        return context

    def get_form(self, *args, **kwargs):
        form = super(NominationCreateView, self).get_form(self.form_class)
        ntype = get_object_or_404(
            NominationType, slug=self.kwargs.get('slug'), active=True)
        if ntype.name == 'Kenneth Gonsalves':
            form.fields.popitem('reason_to_join_board')
        return form

    def __init__(self, *args, **kwargs):
        super(NominationCreateView, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.ntype = get_object_or_404(
            NominationType, slug=self.kwargs.get('slug'), active=True)
        emailer.send_new_nomiation_email(
            user=user,
            instance=form.instance
        )
        return super(NominationCreateView, self).form_valid(form)


class ViewNominationListView(ListView, LoginRequiredMixin):
    model = NominationType
    template_name = 'nominations/nomination_list.html'
    context_object_name = 'nomination_types'

    def dispatch(self, request, *args, **kwargs):
        if not is_board_member(self.request.user):
            return HttpResponseForbidden("Sorry! You do not have permission to view the Nominations!")
        return super(ViewNominationListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(
            ViewNominationListView, self).get_context_data(*args, **kwargs)

        nominations = NominationType.objects.values_list('id', 'name', 'slug').distinct()
        nomination_dict = {}
        for each in nominations:
            nomination_dict[each[0]] = '%s - %s' % (each[1], each[2])

        context['nomination_types'] = nomination_dict

        board_members_list = BoardMember.objects.all() #.filter(end_date__gte=datetime.now())
        board_members = {}
        for member in board_members_list:
            board_members[member.user.id] = member.user.get_full_name()

        context['board_members'] = board_members

        return context


class CreateVoteUrlView(ListView, LoginRequiredMixin):
    model = NominationType
    template_name = 'nominations/nomination_list.html'
    context_object_name = 'nomination_type_list'

    def dispatch(self, request, *args, **kwargs):
        if not is_board_member(self.request.user):
            return HttpResponseForbidden("Sorry! You do not have permission to view the Nominations!")
        return super(CreateVoteUrlView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nom_id = request.POST.get('nomination_id')
        nomination = request.POST.get('nomination')
        nom_type, slug = nomination.split(' - ')
        board_members = request.POST.getlist('board_members[]')
        ntype = get_object_or_404(NominationType, id=nom_id)

        for member in board_members:
            user_obj = get_object_or_404(User, id=int(member))

            # unique hash per user
            data = [user_obj.get_full_name(), user_obj.email, slug, nom_type, datetime.now()]
            
            hash_ = hashlib.md5(pickle.dumps(data, 0)).hexdigest()
            expiry_date = datetime.now() + timedelta(days=10)

            host = '{}://{}'.format(settings.SITE_PROTOCOL,
                                    request.META['HTTP_HOST'])
            url = '%s%s' % (host, reverse('vote_nominee', kwargs={'nomination': nom_id, 'hash': hash_}))

            # store the hash and expiry in DB. Expiry is set to 10 days from date of creation
            voting_url = VotingURL(user=user_obj, url_hash=hash_, expiry=expiry_date, ntype=ntype)
            voting_url.save()

            send_voting_email(user_obj, nom_type, slug, url)

        return HttpResponse('Success')


class ViewNominations(ListView, LoginRequiredMixin):
    model = Nomination
    template_name = 'nominations/nomination_vote.html'
    context_object_name = 'nominees'

    def dispatch(self, request, *args, **kwargs):
        if not is_board_member(self.request.user):
            return HttpResponseForbidden("Sorry! You do not have permission to view the Nominations!")
        return super(ViewNominations, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(
            ViewNominations, self).get_context_data(*args, **kwargs)

        nomination_id = self.kwargs.get('nomination')
        hash_ = self.kwargs.get('hash')

        ntype = get_object_or_404(NominationType, id=nomination_id)

        # logged in user verification
        voting_url_obj = VotingURL.objects.filter(user=self.request.user, url_hash=hash_, ntype=ntype)
        if voting_url_obj:
            voting_url_obj = voting_url_obj[0]
            if voting_url_obj.expiry <= timezone.now():
                context['message'] = 'Sorry! Voting is closed.'
                return context
            # check if the user has already voted
            if UserVoting.objects.filter(voting_url=voting_url_obj).exists():
                context['message'] = 'Sorry! You have already Voted.'
                return context

            nominees = Nomination.objects.filter(ntype=nomination_id)
            context['nominees'] = nominees
            context['nomination'] = '%s - %s' % (ntype.name, ntype.slug)
            context['expiry'] = voting_url_obj.expiry
            context['hash'] = hash_
            context['nomination_id'] = nomination_id
            return context
           
        else:
            context['message'] = 'Sorry! You are not the intended recipient.'
            return context

    def post(self, request, *args, **kwargs):
        nomination_id = self.kwargs.get('nomination')
        hash_ = self.kwargs.get('hash')

        nominee = request.POST.get('nominee')
        comments = request.POST.get('comments')

        ntype = get_object_or_404(NominationType, id=nomination_id)
        voting_url_obj = get_object_or_404(VotingURL, user=self.request.user, url_hash=hash_, ntype=ntype)
        nomination_obj = get_object_or_404(Nomination, id=nominee)

        voting = UserVoting(user=request.user, vote=nomination_obj, voting_url=voting_url_obj, comments=comments)
        voting.save()

        return HttpResponse('Success')

        
class VotingSummaryList(ListView, LoginRequiredMixin):
    model = UserVoting
    template_name = 'nominations/voting_summary.html'
    context_object_name = 'summary'

    def dispatch(self, request, *args, **kwargs):
        if not is_board_member(self.request.user):
            return HttpResponseForbidden("Sorry! You do not have permission to view the Nominations!")
        return super(VotingSummaryList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(
            VotingSummaryList, self).get_context_data(*args, **kwargs)

        nominations = NominationType.objects.values_list('id', 'name', 'slug').distinct()
        nomination_dict = {}
        for each in nominations:
            nomination_dict[each[0]] = '%s - %s' % (each[1], each[2])

        context['nomination_types'] = nomination_dict

        return context

    def post(self, request, *args, **kwargs):

        nomination_id = request.POST.get('nomination_id')
        ntype = get_object_or_404(NominationType, id=nomination_id)

        # get all the nominations for ntype
        nominations = Nomination.objects.filter(ntype=ntype)
        vote_summary = []

        for each_nom in nominations:
            vote_count = UserVoting.objects.filter(vote=each_nom).count()
            vote_summary.append({'name': each_nom.fullname, 'vote_count': vote_count, 'profession': each_nom.profession,
                                                'contribution_info': each_nom.contribution_info})
        return HttpResponse(json.dumps(vote_summary))
