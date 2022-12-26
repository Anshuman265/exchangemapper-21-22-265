from dal import autocomplete
from django import forms
from django.forms import modelformset_factory
from main.models import *
from captcha.fields import CaptchaField
from ckeditor.widgets import CKEditorWidget

seasons = [
    ('None', 'All'),
    ('S', 'Spring'),
    ('A', 'Autumn'),
]

seasons2 = [
    ('S', 'Spring'),
    ('A', 'Autumn'),
]
years = [
    ('None', 'All'),
    ('2', 'Second year'),
    ('3', 'Third year'),
    ('4', 'Fourth year'),
    ('5', 'Dual Degree'),
]

years2 = [
    ('2', 'Second year'),
    ('3', 'Third year'),
    ('4', 'Fourth year'),
    ('5', 'Dual Degree'),
]

Uni = University.objects.all()
Uni_list = [('None', 'All')]
for u in Uni:
    name = u.fullname
    id_of_uni = u.id
    Uni_list.append((id_of_uni, name))

Dept = Department.objects.all()
Dept_list = [('None', 'All')]
for d in Dept:
    code = d.code
    name = d.fullname
    Dept_list.append((code, name))


class CaptchaLoginForm(forms.Form):
    captcha = CaptchaField(label="Enter the captcha")


class InputForm(forms.Form):
    # University = forms.ModelChoiceField(required=False, queryset=University.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),empty_label="All")
    University = forms.ChoiceField(choices=Uni_list)
    semester = forms.ChoiceField(choices=seasons)
    year = forms.ChoiceField(choices=years)
    department = forms.ChoiceField(choices=Dept_list)

"""
class UniversityInputForm(forms.Form):
    fullname = forms.CharField(label='University Name', max_length=100)
    University = forms.ChoiceField(choices=Universities)
"""

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=1000, label="Leave a comment",
                              widget=forms.Textarea(attrs={'autocomplete': 'off','rows':2, 'cols':15}))


class ExperienceForm(forms.Form):
    #para1 = forms.CharField(max_length = 400,widget=CKEditorWidget())
    para1 = forms.CharField(
        max_length=2500, widget=forms.Textarea(attrs={'rows':3, 'cols':15}), label="Introduction")
    para2 = forms.CharField(max_length=2500, widget=forms.Textarea(attrs={'rows':3, 'cols':15}),label="Experience")
    para3 = forms.CharField(max_length=2500, widget=forms.Textarea(attrs={'rows':3, 'cols':15}),label="Conclusion")
    img1 = forms.ImageField(label="Profile picture")
    img2 = forms.ImageField(label="Blog Picture 1")
    img3 = forms.ImageField(label="Blog Picture 2")
    iframe = forms.URLField(required=False)


""""
class UniversityForm(forms.Form):
	fullname = forms.CharField(max_length = 500)
	city = forms.CharField(max_length = 60)
	country = forms.CharField(max_length = 60)
"""
class seasonAndYearForm(forms.Form):
    # University = forms.ModelChoiceField(required=False, queryset=University.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),empty_label="All")
    season = forms.ChoiceField(choices=seasons2)
    year = forms.ChoiceField(choices=years2)

class UniversityOnlyForm(forms.Form):
    University = forms.ModelChoiceField(
        required=True,queryset=University.objects.all())
"""
class seasonOnlyForm(forms.Form):
    University = forms.ModelChoiceField(
        required=True,queryset=University.objects.all())
"""

RemotecourseModelFormset = modelformset_factory(
    RemoteCourse,
    # initial = [{'UserInfo' : }],
    fields=('UserInfo', 'code', 'name','homecourse',),
    # widgets = {'homecourse': autocomplete.ModelSelect2(url='main:your_exp')},
    extra=1,
)


class DoubtForm(forms.Form):
    text = forms.CharField(max_length=1000, label="Query",
                           widget=forms.Textarea(attrs={'rows':2, 'cols':15,'autocomplete': 'off'}))


privacy = [(True, 'Anonymous')]


class AnswerForm(forms.Form):
    text = forms.CharField(max_length=2500, widget=forms.Textarea(
        attrs={'autocomplete': 'off','rows':4, 'cols':15,}))
    anonymous = forms.ChoiceField(choices=privacy, widget=forms.RadioSelect,
                                  required=False, label="Check the button to answer anonymously")


class SearchForm(forms.Form):
    university_search = forms.CharField(
        max_length=500, required=False, label="Search Blogs By University...")


"""
RemotecourseModelFormset = modelformset_factory(
	RemoteCourse,
	fields=('code','name','department','homecourse','season','year','university'),
	extra=1,
	# widgets={
	# 	'name': forms.TextInput(attrs={
	# 		'class':'',
	# 		'placeholder':''
	# 	})
	# }
)
"""
