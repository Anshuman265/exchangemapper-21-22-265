from django.db import models
from django.contrib.auth.models import User
# For current date and time
from django.utils import timezone
# Create your models here.
from django.dispatch import receiver
import os

User.has_usable_password = False
seasons = [
    ('S', 'Spring'),
    ('A', 'Autumn'),
]
years = [
    ('2', 'Second year'),
    ('3', 'Third year'),
    ('4', 'Fourth year'),
    ('5', 'Dual Degree'),
]


class UserInfo(models.Model):
    # link to Django User Model
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='userinfo', blank=True, null=True)

    # additional data from SSO
    name = models.CharField(max_length=200)
    roll_number = models.CharField(max_length=20)
    department = models.CharField(max_length=200, null=True, blank=True)
    join_year = models.IntegerField(null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    degree = models.CharField(max_length=300, null=True, blank=True)
    email_ldap = models.CharField(max_length=200)
    upvoted = models.ManyToManyField('Answer', related_name='upuser')
    downvoted = models.ManyToManyField('Answer', related_name='downuser')

    def __str__(self):
        return self.name


class University(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=500)
    country = models.CharField(max_length=60, default=0, blank=False)

    class Meta:
        ordering = ('fullname',)

    def __str__(self):
        return self.fullname


class Department(models.Model):
    code = models.CharField(max_length=6)
    fullname = models.CharField(max_length=500)
    #university = models.ManyToManyField(University)
    # University = models.ManyToManyField(University)

    class Meta:
        ordering = ('fullname',)

    def __str__(self):
        return (self.fullname)


class HomeCourse(models.Model):
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=400, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.code


class RemoteCourse(models.Model):
    UserInfo = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=400, null=True)
    homecourse = models.ForeignKey(
        HomeCourse, on_delete=models.CASCADE, null=False, blank=False)
    university = models.ForeignKey(
        University, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return(self.name+" - "+" - "+self.university.fullname)


class CourseMap(models.Model):
    UserInfo = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, null=True, blank=True)
    University = models.ForeignKey(
        University, on_delete=models.CASCADE, null=True, blank=True)
    season = models.CharField(
        max_length=1,
        choices=seasons,
        default='S',
    )
    year = models.CharField(
        max_length=1,
        choices=years,
        default='2'
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    remote_courses = models.ManyToManyField(RemoteCourse)

    #department = models.CharField(max_length=400,null=True)
    def __str__(self):
        return (self.UserInfo.name+"'s CourseMap")


class Expierence(models.Model):
    # UserInfo = models.ForeignKey(UserInfo,on_delete=models.CASCADE, null=True, blank=True)
    UserInfo = models.OneToOneField(
        UserInfo, on_delete=models.CASCADE, null=True, blank=True)
    # Blog_text = models.CharField(max_length=400,null=True)
    para1 = models.CharField(max_length=2500, null=True)
    para2 = models.CharField(max_length=2500, null=True)
    para3 = models.CharField(max_length=2500, null=True)
    img1 = models.ImageField(upload_to='images/')
    img2 = models.ImageField(upload_to='images/')
    img3 = models.ImageField(upload_to='images/')
    iframe = models.CharField(max_length=400, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return (self.UserInfo.name+"'s Experience")


@receiver(models.signals.post_delete, sender=Expierence)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.img1:
        if os.path.isfile(instance.img1.path):
            os.remove(instance.img1.path)
    if instance.img2:
        if os.path.isfile(instance.img2.path):
            os.remove(instance.img2.path)
    if instance.img3:
        if os.path.isfile(instance.img3.path):
            os.remove(instance.img3.path)


@receiver(models.signals.pre_save, sender=Expierence)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file1 = sender.objects.get(pk=instance.pk).img1
        old_file2 = sender.objects.get(pk=instance.pk).img2
        old_file3 = sender.objects.get(pk=instance.pk).img3
    except sender.DoesNotExist:
        return False

    new_file1 = instance.img1
    new_file2 = instance.img2
    new_file3 = instance.img3
    if not old_file1 == new_file1:
        if os.path.isfile(old_file1.path):
            os.remove(old_file1.path)
    if not old_file2 == new_file2:
        if os.path.isfile(old_file2.path):
            os.remove(old_file2.path)
    if not old_file3 == new_file3:
        if os.path.isfile(old_file3.path):
            os.remove(old_file3.path)


class Comment(models.Model):
    experience = models.ForeignKey(Expierence, on_delete=models.CASCADE)
    # writer = models.ForeignKey(User, on_delete=models.CASCADE)
    writer = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return (self.writer.name+" commented on " + self.experience.UserInfo.name + "'s Experience")


class Doubt(models.Model):
    student = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return (self.text[0:50])


class Answer(models.Model):
    author = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=2500)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    doubt = models.ForeignKey(Doubt, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (self.doubt.text[0:20] + ' -> ' + self.text[0:20])


#------PENDING--------------#
"""

Delete button functionality
add university search filter in blog

"""


#-----FIXED------------#
"""
Change depratment to list
Add max height condition in blog details
add up icon in voting
Add iirc logo in the login page (UGAC | iirc)
blog detail view first para details of exchange
remove extra scroll bar in landing page
Ask for bg image for landing page
<script src="three.r119.min.js"></script>
<script src="vanta.birds.min.js"></script>
<script>
VANTA.BIRDS({
  el: "#your-element-selector",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00,
  birdSize: 1.50,
  wingSpan: 31.00,
  quantity: 4.00
})
</script>
fix images size in blog
decrease width of doubt/answer accordion box and answer form,new question form
blog post change warning UI
click on image to read more
Blog finalize design 
change mapper dropdown, ask for button
in mapper increase margin-bottom between buttons (ask design team)
try increasing the width of modal
change guide, add popup and close button for additional info (w3Schools for popup)
add a paragraph in guide for intro info (PHd dont include)
Ask for footer
Fix the landing page url
FIx the include nav in landing page
Add coursemap button in mapper itself
Add 'all' when none is selected
Add grid in mapper
"""
# redirect of your_exp
# Department should be textfield in INPUT
# Should display all maps by default
# input taken in course map
# Remote course mei add user field
# Added home dept display in user interface
# Change the input of -----
# Add is verified filter
# Minor Course can be of diff dept --> Maps are being filtered using Home Department only
#Univer - RemoteCourse
# dept - HomeCourses filter added
# Semester should be of our clg ony -->The related homecourses are being queried for filtering , fixed
