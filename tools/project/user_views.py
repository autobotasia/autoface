from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.forms.models import model_to_dict
from management.auth_forms import UserProfileForm


@login_required(login_url='/accounts/login/')
def get_current_user_profile(request):

    if request.user.is_authenticated:
        current_user = request.user
        groups = []
        for group in current_user.groups.all():
            groups.append(str(group))
        groups = ", ".join(groups)

        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=current_user)
            for k in form.fields.keys():
                field = form.fields[k]
                css_addition = ' form-control '
                css_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = css_addition + css_classes

            if form.is_valid():
                form.save()
                messages.success(request, 'Updated profile')
                return HttpResponseRedirect(request.path_info)

        # GET Method
        form = UserProfileForm(instance=current_user)
        user_data = { "is_staff" : current_user.is_staff, "is_active" : current_user.is_active, "is_superuser" : current_user.is_superuser, "last_login" : current_user.last_login, "date_joined" : current_user.date_joined, "email" : current_user.email, "groups" : groups }
        #
        for k in form.fields.keys():
            field = form.fields[k]
            css_addition = ' form-control '
            css_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = css_addition + css_classes

        return render(request, 'user-profile.html', { 'user_data': user_data, 'form': form})

    return HttpResponseRedirect('refuse_access')
