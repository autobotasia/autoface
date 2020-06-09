from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.forms.models import model_to_dict



@login_required(login_url='/accounts/login/')
def get_current_user_profile(request):

    if request.user.is_authenticated:
        current_user = request.user
        # context = model_to_dict(current_user)
        # UserFormSet = modelformset_factory(User, fields=('name', 'title'))
        form = UserChangeForm(instance=current_user)
        for k in form.fields.keys():
            field = form.fields[k]
            css_addition = ' form-control '
            css_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = css_addition + css_classes
            if k == 'last_login' or k == 'email' or k == 'date_joined':
                field.widget.attrs['readonly'] = True
                field.widget.attrs['style'] = 'background-color: #152036'


        if request.method == 'POST':
            form = UserChangeForm(request.POST, instance=current_user)
            for k in form.fields.keys():
                field = form.fields[k]
                css_addition = ' form-control '
                if k == 'last_login' or k == 'email' or k == 'date_joined':
                    field.widget.attrs['readonly'] = True
                    field.widget.attrs['style'] = 'background-color: #152036'

                css_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = css_addition + css_classes

            if form.is_valid():
                form.save()
                messages.success(request, 'Updated profile')
                return HttpResponseRedirect(request.path_info)

        return render(request, 'user-profile.html', {'form': form})

    return HttpResponseRedirect('refuse_access')
