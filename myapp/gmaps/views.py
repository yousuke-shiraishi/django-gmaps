
from .models import User, Gmap
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.db.models import Q
from hashlib import md5
from django.views import View
from .forms import GmapForm, UserForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.core.serializers import serialize
from django.utils.html import escapejs
from django.conf import settings



class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/user_detail.html'

class UserCreateView(CreateView):
    model = User
    template_name = 'user/user_form.html'
    form_class = UserForm
    success_url = reverse_lazy('gmap_list')

    def form_valid(self, form):
        form.instance.password = make_password(form.cleaned_data['password'])
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/user_form.html'
    fields = ['username', 'email', 'birth']
    success_url = reverse_lazy('gmap_list')

    def form_valid(self, form):
        new_password = form.cleaned_data['password']
        if not check_password(new_password, self.object.password):
            form.instance.password = make_password(new_password)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            return HttpResponseForbidden("ユーザ情報を編集する権限がありません")
        return super().dispatch(request, *args, **kwargs)



class GmapListView(ListView):
    model = Gmap
    template_name = 'gmap_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        json_data = serialize('json', context['object_list'])
        context['json_data'] = escapejs(json_data)
        context['google_maps_api_key']= settings.GOOGLE_MAPS_API_KEY
        return context

class GmapCreateOrUpdateView(LoginRequiredMixin, UpdateView):
    model = Gmap
    template_name = 'new.html'
    form_class = GmapForm


    def get_object(self, queryset=None):
        if 'pk' not in self.kwargs:
            return None

        if queryset is None:
            queryset = Gmap.objects.filter(user=self.request.user)

        obj = super().get_object(queryset=queryset)

        if obj.user != self.request.user:
            return None

        return obj


    def get_success_url(self):
        return reverse('gmap_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
            self.object = None
        else:
            self.object = self.get_object()
            if self.object is None:
                return HttpResponseForbidden("Gmapを編集する権限がありません")
        return super().dispatch(request, *args, **kwargs)


class GmapDeleteView(LoginRequiredMixin, DeleteView):
    model = Gmap
    template_name = 'gmap_list.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        
        if self.object.user == self.request.user:
            self.object.delete()
            return JsonResponse({'status': 'success'})
        else:
            return HttpResponseForbidden('Gmapを消す権限がありません')


class GmapsSearchView(View):
    template_name = 'gmap_list.html'

    def get(self, request, *args, **kwargs):
        gmaps = []

        public = request.GET.get('radio_search', False)

        if public == "public":
            username = request.GET.get('username')
            birth_year = request.GET.get('birth_year', "").strip()
            birth_month = request.GET.get('birth_month', "").strip()
            birth_day = request.GET.get('birth_day', "").strip()
            birth = '-'.join([birth_year,birth_month,birth_day])

            if not (birth_year and birth_year.isdigit() and 1900 <= int(birth_year) <= 2051):
                return HttpResponseBadRequest("birth yearが不正な値です")

            if not (birth_month and birth_month.isdigit() and 1 <= int(birth_month) <= 12):
                return HttpResponseBadRequest("birth monthが不正な値です")

            if not (birth_day and birth_day.isdigit() and 1 <= int(birth_day) <= 31):
                return HttpResponseBadRequest("birth dayが不正な値です")

            if not username or not birth:
                return HttpResponseBadRequest("ユーザネームか誕生日が不正な値です")

            gmaps = Gmap.objects.filter(user__username=username, user__birth=birth, magic_word="")
        else:
            if not request.user.is_authenticated:
                return HttpResponse("ログインしないとアクセスできません", status=401)

            email = request.GET.get('email')
            magic_word = request.GET.get('magic_word')
            if magic_word == "" or magic_word is None:
                return HttpResponseBadRequest("非公開のデータなのにmagic_wordが空です")

            if not email or not magic_word:
                return HttpResponseBadRequest("メールかマジックワードが不正です")

            magic_word_hash = md5(magic_word.encode()).hexdigest()
            gmaps = Gmap.objects.filter(user__email=email).filter(Q(magic_word=magic_word_hash) & ~Q(magic_word=""))

        json_data = serialize('json', gmaps)
        safe_json_data = escapejs(json_data)

        return render(request, self.template_name, {'gmaps': gmaps, 'json_data': safe_json_data})
