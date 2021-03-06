from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from desksolutionsbase.forms import OrganizationForm, RegisterForm, ApplicationForm, LookupForm, ContactForm
from account.models import Organization, User, Position
# from .decorators import organization_absent
from django.core.exceptions import ValidationError
from django.core import serializers
from django.core.mail import send_mail

import json
# import folium
# from folium.plugins import Draw

from DeskSolutions import settings
# from .utils import get_ip, get_geo
# from geopy.geocoders import Nominatim
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def OrganizationAction(request):
    context = {}
    create_organization = None
    # if request.session.get('organization'):
    #     del request.session['organization']
    # ip = get_ip(request)
    # ip = '119.160.64.50'
    # # ip = '72.14.207.99'

    # geolocator = Nominatim(user_agent='desksolutionsbase')
    
    # # print(ip)

    # country, o_city, lat, lon = get_geo(ip)
    # print('location', o_city)
    # print('location', country)
    # print('location', lat)
    # print('location', lon)

    # pointA = (lat, lon)

    # m = folium.Map(width=800, height=500, location=pointA, zoom_start=13)
    
    # # folium.Marker([lat, lon], draggable=True,tooltip='Click for more', popup=o_city, 
    # #     icon=folium.Icon(color="purple")).add_to(m.add_child(folium.LatLngPopup()))

    # draw = Draw(
    #     draw_options={
    #         'polyline':False,
    #         'rectangle':True,
    #         'polygon':True,
    #         'circle':False,
    #         'marker':True,
    #         'circlemarker':False},
    #     edit_options={'edit':False})
    # m.add_child(draw)
    # folium.Marker([lat, lon], draggable=True,tooltip='Click for more', popup=o_city, 
    #     icon=folium.Icon(color="purple")).add_to(m.add_child(draw))

    # print(m.add_child(folium.LatLngPopup()))
    # print(folium.LatLngPopup())
    # m.add_child(folium.LatLngPopup())

    

    if request.method == "POST" and request.is_ajax():
        print("request is POST")
        form = OrganizationForm(request.POST, request.FILES)
        user_form = RegisterForm(request.POST or None)
        lookup_form = LookupForm(request.POST or None)
        print(settings.BASE_DIR)
        print(settings.MEDIA_ROOT)
        if form.is_valid():
            print("Organization Form is Valid")

            # org = form.save()
            # print(org)
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            url = form.cleaned_data['url']
            address = form.cleaned_data['org_address']
            logo = request.FILES.get('logo')
            city = form.cleaned_data['city']
            # check_city = geolocator.geocode(city, language='en')
            # if check_city is not None:
            #     print("city is ok")
            #     print(check_city)
            create_organization = Organization.objects.create(
            title=title, description=description, url=url, org_address=address, logo=logo, city=city)
            # create_organization.save()
            
            # get_org = Organization.objects.filter(
            #     title=title)
            # print(get_org)

            # for g in get_org:
            #     print(g)
            # print(get_org)
            # ser_instance = serializers.serialize(
            # 'json', get_org)
            # print(ser_instance)
            # ser_instance = json.dumps(get_org, content_type='application/json')
            # print(ser_instance)
            request.session['organization'] = create_organization.pk
            context['org_id'] = create_organization.pk
            # print(ser_instance)
            print(context['org_id'])
            # form.save()
            # return redirect("signup:signups", args=(request.session['organization'],))
            # return redirect('signup:signups')
            # context['json'] = ser_instance
            # return JsonResponse(context)

        elif user_form.is_valid():
            session_id = request.session.get('organization')
            print("session: " + str(session_id))
            lookup_session = request.session.get('lookup_organization')
            print(lookup_session)
            print(session_id)
            if session_id is not None:
                print("session is not none")
                get_organization = get_object_or_404(Organization,id=session_id)
                user = user_form.save(commit=False)
                user.organization = get_organization
                user.save()
                del request.session['organization']
            # elif lookup_session is not None:
            #     get_organization = get_object_or_404(Organization,id=lookup_session)
            #     user = user_form.save(commit=False)
            #     user.organization = get_organization
            #     user.save()
            #     del request.session['organization']
                return redirect(reverse('admin:index'))
            
                # print(request.session['organization'])
        elif lookup_form.is_valid():
            organization_name = lookup_form.cleaned_data.get('organization_name')
            try:
                qs = Organization.objects.get(title = organization_name)                
                request.session['lookup_organization'] = qs.pk
                check_existance = Organization.objects.filter(user__organization_id=qs.pk).exists()
                if check_existance:
                    context['admin_exist'] = "An admin to this organization already exists. Please Login to your account"
            except Organization.DoesNotExist:
                context['lookup_not_exist'] =  "This organization does not exist"
            return JsonResponse(context, safe=False)
        else:
            print("invalid form")
            # m = m._repr_html_()
            context['register_form'] = form.errors
            context['user_form'] = user_form.errors
            context['lookup_form'] = lookup_form.errors
            # context['map'] = m
            return JsonResponse(context)
    else:
        form = OrganizationForm()
        context['register_form'] = form
        # m = m._repr_html_()
        # context['map'] = m
        user_form = RegisterForm()
        context['user_form'] = user_form
        lookup_form = LookupForm()
        context['lookup_form'] = lookup_form

    return render(request, "desksolutionsbase/signup.html", context)


# @organization_absent
# def signup(request):
#     session_id = request.session.get('organization')
#     if session_id is not None:
#         get_organization = Organization.objects.get(id=session_id)
#         print(get_organization)
#         # get_org = get_object_or_404(Organization, title=url)
#         print("in user signup function")
#         context = {}
#         if request.method == "POST":
#             user_form = RegisterForm(request.POST or None)
#             if user_form.is_valid():
#                 print("form valid")
#                 user = user_form.save(commit=False)
#                 # email = user_form.cleaned_data.get('email')
#                 # first_name = user_form.cleaned_data.get('first_name')
#                 # last_name = user_form.cleaned_data.get('last_name')
#                 # phone = user_form.cleaned_data.get('phone')
#                 # address = user_form.cleaned_data.get('address')

#                 # user = User.objects.create_user(
#                 #     email=email)
#                 # profile = profile_form.save(commit=False)
#                 # org = request.session.get('organization')
#                 # for obj in serializers.deserialize("json", org):
#                 #     print(obj)
#                 # print(org)
#                 # print(user)
#                 # convert_to_obj = json.loads(org)
#                 # print(convert_to_obj)
#                 # print(org.id)
#                 user.organization = get_organization
#                 user.save()
#                 group, created = Group.objects.get_or_create(
#                     name=settings.GROUP_ALLOCATE)

#                 ct = ContentType.objects.get_for_model(Organization)
#                 if created:
#                     permission = Permission.objects.filter(content_type=ct)
#                     for perm in permission:
#                         group.permissions.add(perm)
#                     group.save()
#                     user.groups.add(group)
#                 else:
#                     user.groups.add(group)
#                 # profile.organization = user
#                 # profile.save()
#                 del request.session['organization']
#                 return redirect(reverse('admin:index'))
#                 # print(request.session['organization'])
#             else:
#                 print("invalid form")
#                 context['user_form'] = user_form
#         else:
#             user_form = RegisterForm()
#             context['user_form'] = user_form

#         return render(request, 'desksolutionsbase/register.html', context)


def organizationlist(request):
    context = {}
    organizations = Organization.objects.all()
    positions = Position.objects.all()
    # for i in organizations:
    #     print(i)
    #     positions = Position.objects.filter(organization=i, job_posting=True)
    #     print(positions)
    #     context['positions'] = positions
    context['positions'] = positions
    context['orgs'] = organizations
    n = organizations.count()
    context['range'] = range(1, n)

    if request.method == "POST" and request.is_ajax():
        print("contact form")
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            email = request.POST['contact_email']
            name = request.POST['contact_name']
            message = request.POST['contact_message']
            print(name)
            send_mail(
                "Message",
                message,
                email,
                ["f2018027021@umt.edu.pk",],
                fail_silently=False
            )
        else:
            context['contact_form'] = contact_form.errors
            return JsonResponse(context["contact_form"], status=400)
    else:
        context['contact_form'] = ContactForm()

    return render(request, "desksolutionsbase/base.html", context)

def jobs(request, pk):
    context = {}
    qs = Position.objects.filter(organization=pk, job_posting=True)
    organizations = get_object_or_404(Organization,pk=pk)
    context['jobs'] = qs
    context['orgs'] = organizations

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            print("APPLICATION form valid")
            app_id = request.POST.get('app_id')
            # print(app_id)
            application= form.save(commit=False)
            application.position_id = app_id
            application.save()
            # context['application_form'] = "Success"
            # print(JsonResponse(context['application_form'], safe=False))
        else:
            print("Application form is invalid")
            # form = ApplicationForm()
            context['application_form'] = form.errors
            print(context['application_form'])
            print(JsonResponse(context['application_form']))
            return JsonResponse(context['application_form'])
    else:
        form = ApplicationForm()
        context['application_form'] = form
    return render(request, "desksolutionsbase/jobs.html", context)





