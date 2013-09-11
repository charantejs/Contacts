# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db import transaction
from django.utils import simplejson
from datetime import datetime

from models import *
from forms import *

from pdb import set_trace as trace

current_time = datetime.now()

def index(request):
    return HttpResponse('Hello World')

def search(request):
    results = []
    if request.method == 'GET' and request.GET.get('query',None):
        #trace()
        searchStr = request.GET.get('query',None)
        search_results = PhoneNumber.objects.filter(Q(number__icontains=searchStr) | Q(person__name__icontains=searchStr)).values_list('person__name').distinct()
	print search_results
        results = [ x[0] for x in search_results ]
    	json = simplejson.dumps(results)
    	return HttpResponse(json, mimetype='application/json')
    if request.method == 'POST':
	searchStr = request.POST.get('query',None)
	search_results = PhoneNumber.objects.filter(Q(number__icontains=searchStr) | Q(person__name__icontains=searchStr))
	return render_to_response('search_contacts.html', {'search_results':search_results}, context_instance=RequestContext(request))
    return HttpResponse('Pass some values to search data.')

def display_contacts(request):
    persons = Person.objects.all()
    return render_to_response('display_contacts.html', {'persons':persons}, context_instance=RequestContext(request))


def add_contact(request):
    try:
    	if request.method == "POST":
	    addPersonForm = PersonForm(request.POST)
	    if addPersonForm.is_valid():
	        personObj = addPersonForm.save()
	        for key in request.POST.keys():
		    if key.startswith('phonenumber') and request.POST[key]:
		        phonetype = request.POST['phonetype'+key.split('phonenumber')[1]]
		        phoneNumObj = PhoneNumber(number=request.POST[key],phonetype=phonetype,person=personObj,created_date=current_time)
			phoneNumObj.save()

  		    elif key.startswith('email') and request.POST[key]:
		        emailtype = request.POST['typeofemail'+key.split('email')[1]] 
		        emailObj = Email(email=request.POST[key],emailtype=emailtype,person=personObj,created_date=current_time)
			emailObj.save()

		    elif key.startswith('dateofevent') and request.POST[key]:
		        eventdate = request.POST['dateofevent'+key.split('event')[1]] 
		        eventObj = Event(eventname=request.POST[key],eventdate = eventdate,person=personObj,created_date=current_time)
	    		eventObj.save()

	        transaction.commit()
	        return render_to_response('success.html',{'Msg':'Contact Saved Successfully'},context_instance=RequestContext(request))
        else:
	    addPersonForm = PersonForm()

        context = {'phonetypes':PHONE_TYPES,'emailtypes':EMAIL_TYPES,'eventtypes':EVENT_TYPES,
		'addPersonForm':addPersonForm,'created_date':current_time}
        return render_to_response('contact_add.html',context,context_instance=RequestContext(request))
    except:
	transaction.rollback()
	raise

def view_edit_contact(request,person_id):
    try:
    	personObj = Person.objects.get(id = person_id)
    	phoneObj = PhoneNumber.objects.filter(person__id=person_id)
    	emailObj = Email.objects.filter(person__id=person_id)
    	eventObj = Event.objects.filter(person__id=person_id)
	if request.method == 'POST':
	    updatePersonForm = PersonForm(request.POST, instance=personObj)
	    if updatePersonForm.is_valid():
	        personObj = updatePersonForm.save()
	        for key in request.POST.keys():
		    if key.startswith('phonenumber'):
			phone_id = key.split('phonenumber')[1]
			phonetype = request.POST['phonetype'+str(phone_id)]
			if request.POST[key]:			    
			    upphoneObj = PhoneNumber.objects.filter(id=phone_id,person=personObj)
			    if not upphoneObj:
				phoneNumObj = PhoneNumber(number=request.POST[key],phonetype=phonetype,person=personObj,created_date=current_time)
				phoneNumObj.save()
			    upphoneObj.update(number=request.POST[key],phonetype=phonetype,modified_date=current_time)
			else:
			    PhoneNumber.objects.filter(id=phone_id).delete()

  		    elif key.startswith('email'):
			email_id = key.split('email')[1]
			emailtype = request.POST['typeofemail'+str(email_id)]
			if request.POST[key]:			    
			    upemailObj = Email.objects.filter(id=email_id,person=personObj)
			    if not upemailObj:
				emailObj = Email(email=request.POST[key],emailtype=emailtype,person=personObj,created_date=current_time)
				emailObj.save()
		            upemailObj.update(email=request.POST[key],emailtype=emailtype,modified_date=current_time)
			else:
			    Email.objects.filter(id=email_id).delete()

		    elif key.startswith('dateofevent'):
			event_id = key.split('event')[1]
			eventdate = request.POST['dateofevent'+str(event_id)]
			if request.POST[key]:
			    upeventObj = Event.objects.filter(id=event_id,person=personObj) 
			    if not upeventObj:
				eventObj = Event(eventname=request.POST[key],eventdate = eventdate,person=personObj,created_date=current_time)
	    			eventObj.save()
		            upeventObj.update(eventname=request.POST[key],eventdate = eventdate,modified_date=current_time)
	    		else:
			    Event.objects.filter(id=event_id).delete()

	        transaction.commit()
	        return render_to_response('success.html',{'Msg':'Contact Saved Successfully'},context_instance=RequestContext(request))
        else:
	    updatePersonForm = PersonForm(instance=personObj)
    	context = {'phonetypes':PHONE_TYPES,'emailtypes':EMAIL_TYPES,'eventtypes':EVENT_TYPES,
		'personObj':personObj,'phoneObj':phoneObj,'emailObj':emailObj,'eventObj':eventObj,
		'updatePersonForm':updatePersonForm}
    	return render_to_response('view_edit_contact.html', context, context_instance=RequestContext(request))
    except Exception, e:
	return HttpResponse('cant update ur contact now.',e)


def delete_contact(request,person_id):
    try:
	#trace()
    	personObj = Person.objects.get(id=person_id)
    	if request.method == "POST":
	    if Event.objects.filter(person=personObj):
		Event.objects.filter(person=personObj).delete()
	    if PhoneNumber.objects.filter(person=personObj):
		PhoneNumber.objects.filter(person=personObj).delete()
	    if Email.objects.filter(person=personObj):
		Email.objects.filter(person=personObj).delete()
	    personObj.delete()
	    return render_to_response('success.html',{'Msg':'Contact Deleted Successfully'},context_instance=RequestContext(request))
    	return render_to_response('confirm.html',{'personObj':personObj},context_instance=RequestContext(request))
    except ObjectDoesNotExist:
	transaction.roolback()
	return HttpResponse('Objects Not Does Not Exist')


def display_groups(request):
    groups = PhoneGroup.objects.all()
    return render_to_response('display_groups.html', {'groups':groups}, context_instance=RequestContext(request))

def view_groupdetails(request,group_id):
    try:
    	group = PhoneGroup.objects.get(id=group_id)
    	group_details = Person.objects.select_related('groups').filter(groups__id=group_id)
    	return render_to_response('group_details.html', {'group':group,'group_details':group_details}, context_instance=RequestContext(request))
    except ObjectDoesNotExist:
	return HttpResponse('Objects Not Does Not Exist')

def add_group(request):
    if request.method == "POST":
	name = request.POST.get('groupname',None)
	if not PhoneGroup.objects.filter(name=name):
	    groupObj = PhoneGroup(name=name,created_date=current_time)
	    groupObj.save()
	    return render_to_response('success.html',{'Msg':'Group Saved Successfully'},context_instance=RequestContext(request))
        else:
    	    return render_to_response('group_add.html',{'created_date':current_time,'error':'This Group already exist.'},context_instance=RequestContext(request))
    return render_to_response('group_add.html',{'created_date':current_time},context_instance=RequestContext(request))

def edit_group(request,group_id):
    try:
    	groupObj = PhoneGroup.objects.get(id=group_id)
    	if request.method == "POST":
	    name = request.POST.get('groupname',None)
	    old_name = request.POST.get('groupname-old',None)
	    if name == old_name:
	    	PhoneGroup.objects.filter(id=group_id).update(name=name,modified_date=current_time)
		return render_to_response('success.html',{'Msg':'Group Edited Successfully'},context_instance=RequestContext(request))
	    elif not PhoneGroup.objects.filter(id=group_id):
		PhoneGroup.objects.filter(name=old_name).update(name=name,modified_date=current_time)
		return render_to_response('success.html',{'Msg':'Group Edited Successfully'},context_instance=RequestContext(request))
	    else:
    	    	return render_to_response('group_add.html',{'created_date':current_time,'error':'This Group already exist.'},context_instance=RequestContext(request))
        return render_to_response('group_edit.html',{'groupObj':groupObj},context_instance=RequestContext(request))
    except ObjectDoesNotExist:
	return HttpResponse('Object Does Not Exist33')

def delete_group(request,group_id):
    groupObj = PhoneGroup.objects.filter(id=group_id)
    if request.method == "POST":
	groupObj.delete()
	return render_to_response('success.html',{'Msg':'Group Deleted Successfully'},context_instance=RequestContext(request))
    return render_to_response('confirm.html',{'groupObj':groupObj},context_instance=RequestContext(request))


def add_relation(request):
    if request.method == "POST":
	name = request.POST.get('relationshipname',None)
	if not RelationShip.objects.filter(name=name):
	    relationObj = RelationShip(name=name,created_date=current_time)
	    relationObj.save()
	    return render_to_response('success.html',{'Msg':'Relationship Saved Successfully'},context_instance=RequestContext(request))
	else:
    	    return render_to_response('relation_add.html',{'created_date':current_time,'error':'This Relationship already exist.'},context_instance=RequestContext(request))
    return render_to_response('relation_add.html',{},context_instance=RequestContext(request))




'''
def add_phonenumber(request):
    #trace()
    if request.method == "POST":
	addPhoneNumberForm = PhoneNumberForm(request.POST)
	if addPhoneNumberForm.is_valid():
	    addPhoneNumberForm.save()
	    return render_to_response('success.html',{'Msg':'Phonenumber Saved Successfully'},context_instance=RequestContext(request))
    else:
	addPhoneNumberForm = PhoneNumberForm()
    return render_to_response('phonenumber_add.html',{'addPhoneNumberForm':addPhoneNumberForm},context_instance=RequestContext(request))

def edit_phonenumber(request):
    return render_to_response('phonenumber_edit.html',{},context_instance=RequestContext(request))

def delete_phonenumber(request):
    return render_to_response('phonenumber_delete.html',{},context_instance=RequestContext(request))

def add_email(request):
    #trace()
    if request.method == "POST":
	addEmailForm = EmailForm(request.POST)
	if addEmailForm.is_valid():
	    addEmailForm.save()
	    return render_to_response('success.html',{'Msg':'Email Saved Successfully'},context_instance=RequestContext(request))
    else:
	addEmailForm = EmailForm()
    return render_to_response('email_add.html',{'addEmailForm':addEmailForm},context_instance=RequestContext(request))

def edit_email(request):
    return render_to_response('email_edit.html',{},context_instance=RequestContext(request))

def delete_email(request):
    return render_to_response('email_delete.html',{},context_instance=RequestContext(request))

def add_event(request):
    #trace()
    if request.method == "POST":
	addEventForm = EventForm(request.POST)
	if addEventForm.is_valid():
	    addEventForm.save()
	    return render_to_response('success.html',{'Msg':'Event Saved Successfully'},context_instance=RequestContext(request))
    else:
	addEventForm = EventForm()
    return render_to_response('event_add.html',{'addEventForm':addEventForm},context_instance=RequestContext(request))

def edit_event(request):
    return render_to_response('event_edit.html',{},context_instance=RequestContext(request))

def delete_event(request):
    return render_to_response('event_delete.html',{},context_instance=RequestContext(request))

'''
