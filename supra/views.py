# -​*- coding: utf-8 -*​-
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, DeleteView
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import inlineformset_factory, modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q, F
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseBadRequest
from django.conf.urls import include, url
from django.contrib.auth import authenticate, login, logout
from django import forms
import sys
import inspect
import datetime
from django.core import serializers
import json
from auths import SupraAuthenticationMixin
from django.db import models
from django.db.models import fields
from decimal import Decimal
from django.db.models.fields.files import ImageFieldFile, FieldFile
from django.middleware.csrf import get_token

"""
	@name: SupraConf
	@author: exile.sas
	@date: 21/02/2016
	@licence: creative commons
"""


class SupraConf:
    body = False
    template = False
    date_format = "%d/%m/%Y"
    datetime_format = "%d/%m/%Y %I:%M%p"
    time_format = "%I:%M%p"
    content_type = "application/json; charset=utf-8"

    ACCECC_CONTROL = {
        "allow": False,
        "origin": "*",
        "credentials": "true",
        "headers": "accept, content-type",
        "max_age": "1728000",
        "methods": "POST, GET, OPTIONS, DELETE"
    }

# end class


def access_control(old):
    def new(request, *args, **kwargs):
        httpresponse = old(request, *args, **kwargs)
        if SupraConf.ACCECC_CONTROL['allow'] and isinstance(httpresponse, HttpResponse):
            origin = SupraConf.ACCECC_CONTROL['origin']
            if not isinstance(request, dict):
                if 'HTTP_ORIGIN' in request.META:
                    host = request.META['HTTP_ORIGIN']
                else:
                    host = request.META['HTTP_HOST']
                    if request.is_secure():
                        host = "https://" + host
                    else:
                        host = "http://" + host
                    # end if
                # end if
                print host
                if origin == '*' or (isinstance(origin, list) and host in origin):
                    origin = host
                else:
                    origin = ""
                # end if
            # end if
            httpresponse["Access-Control-Allow-Origin"] = origin
            httpresponse["Access-Control-Allow-Credentials"] = SupraConf.ACCECC_CONTROL['credentials']
            httpresponse["Access-Control-Allow-Headers"] = SupraConf.ACCECC_CONTROL['headers']
            httpresponse["Access-Control-Max-Age"] = SupraConf.ACCECC_CONTROL['max_age']
            httpresponse["Access-Control-Allow-Methods"] = SupraConf.ACCECC_CONTROL['methods']
        # end if
        return httpresponse
    # end def
    return new
# end def

"""
	@name: SupraListView
	@author: exile.sas
	@date: 13/10/2015
	@licence: creative commons
"""


class SupraListView(ListView, SupraAuthenticationMixin):
    list_display = None
    search_fields = []
    list_filter = []
    kwargs = {}
    dict_only = False
    rules = {}
    template = False
    template_name = "supra/list.html"
    request = None
    search_key = 'search'
    date_format = SupraConf.date_format
    datetime_format = SupraConf.datetime_format
    time_format = SupraConf.time_format

    @classmethod
    def as_url(cls):
        app = cls.model.__name__.lower()
        return url('%s/list/$' % (app, ), cls.as_view(),)
    # end class

    def __ini__(self, dict_only=False, *args, **kwargs):
        self.dict_only = dict_only
        return super(SupraListView, self).__init__(*args, **kwargs)
    # end def

    @method_decorator(access_control)
    def dispatch(self, request, *args, **kwargs):
        
        auth = self.auth(request, *args, **kwargs)
        if auth:
            return auth
        # end if
        kwargs = self.get_list_kwargs(request)
        self.template = request.GET.get('template', SupraConf.template)
        self.request = request
        return super(SupraListView, self).dispatch(request, *args, **kwargs)
    # end def

    def get_kwargs(self, request):
        kwargs = {}
        if request.method in ('GET',):
            kwargs = request.GET
        # end def
        return kwargs
    # end def

    def get_list_kwargs(self, request):
        kwargs = self.get_kwargs(request)
        for field in self.list_filter:
            if field in kwargs:
                kwarg = kwargs[field]
                self.kwargs[field] = kwarg
            # end if
        # end for
        if self.search_key in kwargs:
            self.kwargs[self.search_key] = kwargs[self.search_key]
        # end def
        return kwargs
    # end def

    def get_queryset(self):
        queryset = super(SupraListView, self).get_queryset()
        q = Q()
        for column in self.list_filter:
            if column in self.kwargs:
                filter = self.kwargs[column]
                kwargs = {
                    column: filter,
                }
                q = Q(q & Q(**kwargs))
            # end if
            queryset = queryset.filter(q)
        # end for
        q = False
        if self.search_key in self.kwargs:
            for column in self.search_fields:
                search = self.kwargs[self.search_key]
                kwargs = {
                    '{0}__{1}'.format(column, 'icontains'): search,
                }
                if q:
                    q = q | Q(**kwargs)
                else:
                    q = Q(**kwargs)
                # end if
            # end for
            if not q:
                raise Exception('The view has not defined any search_fields')
            # end if
            queryset = queryset.filter(q)
        # end if
        queryset = queryset.filter(**self.rules)
        return queryset
    # end def

    def get_context_data(self, **kwargs):
        context = super(SupraListView, self).get_context_data(**kwargs)
        context['num_rows'] = context['object_list'].count()
        context['object_list'] = context['object_list']
        return context
    # end def

    def get_object_list(self, object_list):
        queryset = object_list
        self_list = []
        list_display = []
        if self.list_display:
            for i in range(len(self.list_display)):
                display = self.list_display[i]
                if isinstance(display, tuple):
                    if hasattr(self, display[0]):
                        self_list.append(display)
                    else:
                        list_display.append(display)
                    # end if
                elif hasattr(self, display):
                    self_list.append(display)
                else:
                    list_display.append(display)
                # end def
            # end for
            if hasattr(self, 'Renderer'):
                renderers = dict((key, F(value)) for key, value in self.Renderer.__dict__.iteritems(
                ) if not callable(value) and not key.startswith('__'))
                queryset = queryset.annotate(**renderers)
            # end if
        # end if

        def extra(dct, objlist, index, row):
            obj = list(objlist)[index]
            
            for slf in self_list:
                if isinstance(slf, tuple):
                    encode = slf[1]
                    slf = slf[0]
                else:
                    encode = None
                # end if
                attr = getattr(self, slf)
                if callable(attr):
                    dct[slf] = attr(obj, row)
                else:
                    dct[slf] = attr
                # end if
                if encode == 'json':
                    dct[slf] = json.loads(dct[slf])
                # end if
            # end for
            return dct
        # end def
        return self.format_json(queryset, extra, list_display=list_display)
    # end def

    @classmethod
    def format_json(cls, queryset, extra=None, time=0, list_display=[]):
        from django.db.models.query import QuerySet
        object_list = []

        if isinstance(queryset, QuerySet):
            list_d = []
            for lis in list_display:
                if isinstance(lis, tuple):
                    list_d.append(lis[0])
                else:
                    list_d.append(lis)
                # end if
            # end for
            rows = queryset.values(*list_d)
        else:
            rows = queryset
        # end if
        i = 0
        for row in rows:
            dct = {}

            if isinstance(row, dict):
                if isinstance(queryset[i], dict) and not 'pk' in queryset[i]:
                    pk = queryset[i].pk
                    row['pk'] = pk
                # end if
            # end if
            obj = row

            if list_display == [] or list_display == None:
                if isinstance(row, dict):
                    list_display = row
                else:
                    list_display = row.__dict__
                    row = row.__dict__
                # end if
            # end if
            for col in list_display:
                if isinstance(col, tuple):
                    encode = col[1]
                    col = col[0]
                else:
                    encode = None
                # end if

                if col != '_state' and col in row:
                    val = row[col]
                else:
                    val = None
                # end if

                if encode == 'json':
                    if isinstance(val, dict) or isinstance(val, list):
                        dct[col] = val
                    else:
                        dct[col] = json.loads(val)
                    # end if
                elif isinstance(val, Decimal):
                    dct[col] = unicode(val)
                elif isinstance(val, datetime.datetime):
                    dct[col] = val.strftime(cls.datetime_format)
                elif isinstance(val, datetime.date):
                    dct[col] = val.strftime(cls.date_format)
                elif isinstance(val, datetime.time):
                    dct[col] = val.strftime(cls.time_format)
                elif isinstance(val, dict) or isinstance(val, list):
                    dct[col] = cls.format_json(val, extra, time=time + 1)
                elif hasattr(val, 'all'):
                    dct[col] = cls.format_json(val.all(), extra, time=time + 1)
                elif isinstance(val, models.Model):
                    dct[col] = unicode(val)
                elif isinstance(val, ImageFieldFile):
                    if val:
                        dct[col] = str(val.url)
                    else:
                        dct[col] = None
                    # end if
                elif isinstance(val, FieldFile):
                    if val:
                        dct[col] = str(val.url)
                    else:
                        dct[col] = None
                    # end if
                else:
                    dct[col] = val
                # end if
                #setattr(obj, col, dct[col])
            # end for
            if extra and callable(extra):
                dct = extra(dct, queryset, i, row)
            # end if
            object_list.append(dct)
            i = i + 1
        # end for
        return object_list
    # end def

    @method_decorator(access_control)
    def render_to_response(self, context, **response_kwargs):
        json_dict = {}

        object_list = self.get_object_list(context["object_list"])

        page_obj = context["page_obj"]
        paginator = context["paginator"]
        num_rows = context["num_rows"]
        if page_obj:
            if page_obj.has_previous():
                json_dict["previous"] = page_obj.previous_page_number()
            # end if
            if page_obj.has_next():
                json_dict["next"] = page_obj.next_page_number()
            # endif
        # end if
        if paginator:
            json_dict["count"] = paginator.count
            json_dict["num_pages"] = paginator.num_pages
            json_dict["page_range"] = str(paginator.page_range)
        # end if
        json_dict["num_rows"] = num_rows
        json_dict["object_list"] = object_list
        if self.dict_only:
            return json_dict
        # end if
        if self.template:
            json_dict['search_fields'] = self.search_fields
            return render(self.request, self.template_name, json_dict)
        # end if
        return HttpResponse(json.dumps(json_dict, cls=DjangoJSONEncoder, ensure_ascii=False), content_type=SupraConf.content_type)
    # end def

# end class


class SupraDetailView(DetailView, SupraAuthenticationMixin):
    fields = None
    extra_fields = {}
    template_name = "supra/list.html"
    dict_only = False

    @classmethod
    def as_url(cls):
        app = cls.model.__name__.lower()
        return url(r'^%s/(?P<pk>\d+)/$' % (app, ), cls.as_view(), )
    # end class

    def __ini__(self, dict_only=False, *args, **kwargs):
        self.dict_only = dict_only
        return super(SupraDetailView, self).__init__(*args, **kwargs)
    # end def

    @method_decorator(access_control)
    def dispatch(self, request, *args, **kwargs):
        auth = self.auth(request, *args, **kwargs)
        self.kwargs = kwargs
        if auth:
            return auth
        # end if
        if hasattr(self, 'Renderer'):
            renderers = dict((key, value) for key, value in self.Renderer.__dict__.iteritems(
            ) if not key.startswith('__'))
            for renderer in renderers:
                listv = renderers[renderer](dict_only=True)
                ref = self.get_reference(listv)
                if ref:
                    pk = kwargs['pk']
                    listv.rules[ref.name] = pk
                    self.extra_fields[renderer] = listv.dispatch(
                        request, *args, **kwargs)
                # end def
            # end for
        # end if
        return super(SupraDetailView, self).dispatch(request, request, *args, **kwargs)
    # end def

    def get_reference(self, listv):
        for field in listv.model._meta.fields:
            if field.is_relation and field.rel.to == self.model:
                return field
            # end if
        # end for
        return False
    # end def

    def render_to_response(self, context, **response_kwargs):
        json_dict = {}
        if self.fields:
            for field in self.fields:
                json_dict[field] = getattr(context["object"], field)
            # end for
        else:
            fields = context["object"]._meta.fields
            for field in fields:
                json_dict[field.name] = getattr(context["object"], field.name)
            # end for
        # end if
        for extra in self.extra_fields:
            json_dict[extra] = self.extra_fields[extra]
        # end for
        json_dict['pk'] = context["object"].pk
        json_dict = SupraListView.format_json([json_dict])
        if self.dict_only:
            return json_dict[0]
        # end if
        return HttpResponse(json.dumps(json_dict[0], cls=DjangoJSONEncoder), content_type=SupraConf.content_type)
    # enddef
# end class


class SupraFormView(FormView, SupraAuthenticationMixin):
    template_name = "supra/form.html"
    response_json = True
    inlines = []
    validated_inilines = []
    invalided_inilines = []
    body = False
    http_kwargs = {}
    initial_pk = None

    @classmethod
    def as_url(cls):
        app = cls.model.__name__.lower()
        urlpatterns = [
            url(r'^%s/form/(?P<pk>\d+)/$' % (app, ), cls.as_view()),
            url(r'^%s/form/$' % (app, ), cls.as_view()),
        ]
        return url(r'^', include(urlpatterns))
    # end class

    @method_decorator(access_control)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        body = request.body
        self.body_data = request.POST.get('body',  body)
        auth = self.auth(request, *args, **kwargs)
        if auth:
            return auth
        # end if
        self.http_kwargs = kwargs
        return super(SupraFormView, self).dispatch(request, *args, **kwargs)
    # end def

    def get_form_class(self):
        if not self.form_class:
            class SupraDefaultFromClass(forms.ModelForm):

                class Meta:
                    model = self.model
                    exclude = []
                # end class
            # end class
            self.form_class = SupraDefaultFromClass
        # end if
        return self.form_class
    # end def

    def get_form_kwargs(self):
        kwargs = super(SupraFormView, self).get_form_kwargs()
        if 'pk' in self.http_kwargs:
            self.initial_pk = self.http_kwargs['pk']
        # end if
        if (self.body or SupraConf.body) and self.request.method in ('POST', 'PUT'):
            try:
                body = json.loads(self.body_data)
                kwargs.update({
                    'data': body
                })
            except ValueError as e:
                pass
            # end try
        # end def
        kwargs['instance'] = self.get_instance(kwargs)
        return kwargs
    # end def

    def get_instance(self, kwargs):
        if self.initial_pk:
            self.instance = self.model.objects.filter(
                pk=self.initial_pk).first()
            if self.instance is None:
                raise Http404
            # end if
        # end if
        if hasattr(self, 'instance'):
            return self.instance
        # end if
        return None
    # end def

    def form_valid(self, form):
        instance = form.save()
        for inline in self.validated_inilines:
            inline.instance = instance
            inline.save()
        # end for
        if self.response_json:
            json_dict = SupraListView.format_json([instance])
            json_dict[0]["session_key"] = self.request.session.session_key
            json_dict[0]["csrf_token"] = get_token(self.request)
            return HttpResponse(json.dumps(json_dict[0]), status=200, content_type=SupraConf.content_type)
        else:
            return HttpResponse(status=200)
        # end if
    # end def

    def get_context_data(self, **kwargs):
        context = super(SupraFormView, self).get_context_data(**kwargs)
        context['inlines'] = []
        for inline in self.inlines:
            if not inline.base_model:
                inline.base_model = self.model
            # end if
            if hasattr(self, 'instance'):
                form_class = inline(request=self.request,
                                    instance=self.instance).get_form()
            else:
                form_class = inline().get_form_class()
            # end if
            context['inlines'].append(form_class)
        # end for
        return context
    # end def

    @method_decorator(csrf_exempt)
    @method_decorator(access_control)
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        is_valid_form = form.is_valid()
        is_valid_inlines = self.is_valid_inlines()
        if is_valid_form and is_valid_inlines:
            return self.form_valid(form)
        # end if
        return self.form_invalid(form)
    # end def

    def is_valid_inlines(self):
        self.invalided_inilines = []
        self.validated_inilines = []
        for inline in self.inlines:
            i = inline()
            i.base_model = self.model
            form_class = i.get_form_class()
            form = form_class(**self.get_form_kwargs())
            if not form.is_valid():
                self.invalided_inilines.append(form)
            # end if
            self.validated_inilines.append(form)
        # end for
        if len(self.invalided_inilines) > 0:
            return False
        # end if
        return True
    # end for

    def form_invalid(self, form):
        errors = dict(form.errors)
        for i in self.invalided_inilines:
            errors['inlines'] = list(i.errors)
        # end for
        return HttpResponse(json.dumps(errors), status=400, content_type=SupraConf.content_type)
    # end def

# end class


class SupraSession(SupraFormView, SupraAuthenticationMixin):
    model = User

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        auth = self.auth(request, *args, **kwargs)
        if auth:
            return auth
        # end if
        this = self

        class SupraDefaultFromClass(forms.ModelForm):

            class Meta:
                model = self.model
                fields = ['username', 'password']
            # end class

            def clean(self):
                return self.data
            # end def

            def save(self, commit=True):
                return this.login(request, self.cleaned_data,)
            # end def
        # end class
        self.form_class = SupraDefaultFromClass

        return super(SupraSession, self).dispatch(request, *args, **kwargs)

    # end def

    def login(self, request, cleaned_data):
        user = authenticate(username=cleaned_data[
                            'username'], password=cleaned_data['password'])
        if user is not None:
            exist_obj = self.model.objects.filter(pk=user.pk).count()
            if exist_obj and user.is_active:
                login(request, user)
                return user
            # end if
        # end if
        raise Http404
    # end def

    def delete(self, request):
        logout(request)
        return HttpResponse(status=200)
    # end def
# end class


class SupraInlineFormView(SupraFormView, SupraAuthenticationMixin):
    base_model = None
    model = None
    formset_class = None
    form_class = None
    instance = None
    no_auto_add = True

    def get_base_model(self):
        return self.base_model
    # end class

    def get_instance(self, kwargs):
        if self.initial_pk:
            self.instance = self.get_base_model().objects.filter(pk=self.initial_pk).first()
            if self.instance is None:
                raise Http404
            # end if
        # end if
        return self.instance
    # end def

    def get_form_class(self):
        if self.formset_class and self.form_class:
            return inlineformset_factory(self.get_base_model(), self.model, form=self.form_class, formset=self.formset_class, exclude=[], extra=2, instance=None)
        else:
            return inlineformset_factory(self.get_base_model(), self.model, exclude=[])
        # end if
    # end def
# end class


class SupraDeleteView(DeleteView, SupraAuthenticationMixin):
    template_name = "supra/delete.html"

    @classmethod
    def as_url(cls):
        app = cls.model.__name__.lower()
        return url(r'^%s/delete/(?P<pk>\d+)/$' % (app, ), cls.as_view())
    # end class

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(status=200)
    # end def

# end class


class SupraCRUD():
    model = None

    list_display = None
    list_filter = []
    search_fields = None
    search_key = None
    form_class = None

    inlines = []
    auto_inlines = []

    @classmethod
    def as_view(cls):

        for auto in cls.auto_inlines:
            class SupraDefaultInlineFormView(SupraInlineFormView):
                model = auto
                base_model = cls.model
            # end class
            cls.inlines.append(SupraDefaultInlineFormView)
        # end class

        class List(SupraListView):
            model = cls.model

            list_display = cls.list_display
            list_filter = cls.list_filter
            search_fields = cls.search_fields
            search_key = cls.search_key
        # end class

        class Form(SupraFormView):
            model = cls.model

            form_class = cls.form_class
            inlines = cls.inlines
        # end class

        class Delete(SupraDeleteView):
            model = cls.model
        # end class

        class Detail(SupraDetailView):
            model = cls.model
        # end class
        app = cls.model.__name__.lower()
        urlpatterns = [
            Detail.as_url(),
            List.as_url(),
            Form.as_url(),
            Delete.as_url(),
        ]
        return include(urlpatterns)

    # end class

    @classmethod
    def as_url(cls):
        return url(r'^', cls.as_view())
    # end class

# end class


def all_supras(view):
    def is_for_supra(obj):
        if inspect.isclass(obj):
            return not hasattr(obj, 'no_auto_add')
        # end if
        return False
    # end def
    supras = inspect.getmembers(sys.modules[view.__name__], is_for_supra)
    urls = []
    for name, supra in supras:
        urls.append(supra.as_url())
    # end for
    return urls
# end def
