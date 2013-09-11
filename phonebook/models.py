from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django.utils import timezone
# Create your models here.
class PhoneGroup(models.Model):
    name = models.CharField(max_length = 45, unique=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('PhoneGroup')
        verbose_name_plural = _('PhoneGroups')
        ordering = ['name']

    def __unicode__(self):
        return self.name

class RelationShip(models.Model):
    name = models.CharField(max_length = 45, unique=True)
    created_date = models.DateTimeField() 
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('RelationShip')
        verbose_name_plural = _('RelationShips')
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=75)
    image = models.ImageField(upload_to='/tmp/', blank=True, null=True)
    groups = models.ManyToManyField(PhoneGroup, blank=True, null=True, help_text=_('The groups this user belongs to.'))
    organisation = models.CharField(max_length = 150,  blank=True, null=True)
    relation = models.ForeignKey(RelationShip,  blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        ordering = ['name']

    def __unicode__(self):
        return self.name


PHONE_TYPES= ['work','mobile','fax','pager','home','other']
PHONE_TYPE_CHOICES= tuple([(TYPE, TYPE.title()) for TYPE in PHONE_TYPES])

class PhoneNumber(models.Model):
    number = models.CharField(max_length = 15)
    phonetype = models.CharField( max_length=30, choices=PHONE_TYPE_CHOICES, default='moile')
    person = models.ForeignKey(Person)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('PhoneNumber')
        verbose_name_plural = _('PhoneNumbers')
        ordering = ['number']

    def __unicode__(self):
        return self.number


EMAIL_TYPES = ['personal','official','other']
EMAIL_TYPE_CHOICES = tuple([(TYPE, TYPE.title()) for TYPE in EMAIL_TYPES])

class Email(models.Model):
    email = models.EmailField(max_length=254)
    emailtype = models.CharField(max_length = 30, choices=EMAIL_TYPE_CHOICES, default='personal')
    person = models.ForeignKey(Person)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Email')
        verbose_name_plural = _('Emails')

    def __unicode__(self):
        return self.email


EVENT_TYPES = ['anniversary','birthday','other']
EVENT_TYPE_CHOICES = tuple([(TYPE, TYPE.title()) for TYPE in EVENT_TYPES])

class Event(models.Model):
    eventname = models.CharField(max_length=30,choices=EVENT_TYPE_CHOICES, default='birthday')
    eventdate = models.DateField()
    person = models.ForeignKey(Person)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        unique_together = (('eventname', 'eventdate','person'),)

    def __unicode__(self):
        return self.eventname
