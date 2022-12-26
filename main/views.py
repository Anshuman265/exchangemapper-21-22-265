from django.db.models.aggregates import Count
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from django.db.models import Count
# import generic views
from django.views.generic import ListView, DetailView

# imports for authentication
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

# other imports
from django.db.models import Q   # finding average rating for a course
#from .lists import *


# Create your views here. function based views, we'll be creating a function for each view
@login_required
def landingpage(request):
    current_name = request.user.userinfo.name
    template_name = 'main/new_nav.html'
    return render(request, template_name, {'current_name': current_name})


def render_login_button(request):
    """ Show 'login with SSO' button if user is not logged in. """
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CaptchaLoginForm(request.POST)
            if form.is_valid():
                human = True
                return redirect('sso:login')
                print('hola')
        else:
            form = CaptchaLoginForm()
        return render(request, 'main/login_new.html', {'form': form})
    else:
        current_name = request.user.userinfo.name
        template_name = 'main/landing_page_new.html'
        return render(request, template_name, {'current_name': current_name})


@login_required
def home(request):
    form = InputForm(request.POST or None)
    semester_code = request.GET.get('semester')
    year = request.GET.get('year')
    department = request.GET.get('department')
    university_id = request.GET.get('University')
    """
        if request.GET.get('department'):
            department = request.GET.get('department')
        
        university_id = "University"
        if request.GET.get('University') == '':
           print("Uni is none")
        if request.GET.get('University'):
            university_id = request.GET.get('University')
        #print(university_id + " " + department)
        if university_id != 'University' and university_id is not None:
        university_in_query = University.objects.filter(id = university_id)
        exp = exp.filter(University__in = university_in_query) #in was important here
    """
    exp = CourseMap.objects.all()  # Without filter data
    exp = exp.filter(is_verified=True)  # Verification filter
    if university_id != 'None' and university_id is not None:
        university_in_query = University.objects.filter(id=university_id)
        # in was important here
        exp = exp.filter(University__in=university_in_query)
    if department != 'None' and department is not None:
        # exp = exp.filter(UserInfo__department__icontains = department) #in was important here
        department = Department.objects.get(code=department)
        # all_remote_courses = RemoteCourse.objects.filter( UserInfo__department=department.fullname)
        exp = exp.filter(department = department).distinct()
    if year != 'None' and year is not None:
        # year=2 is what we recieve
        # all_remote_courses = RemoteCourse.objects.filter(homecourse__year__in=year)
        # distinct() returns only one filter here
        exp = exp.filter(year = year).distinct()
    if semester_code != 'None' and semester_code is not None:
        # semester=S is what we recieve means spring
        # all_remote_courses = RemoteCourse.objects.filter( homecourse__season__in=semester_code)
        exp = exp.filter(season = semester_code).distinct()
    passon = {
        'p': exp,
    }
    return render(request, "main/form.html", {'form': form, 'passon': passon})


@login_required
def blog(request):
    return render(request, 'main/blog.html')


def team_view(request):
    return render(request, 'main/team.html')


@login_required
def yourExperience(request):
    template_name = 'main/formset_view.html'
    # current_name = request.user.userinfo.name
    result = HomeCourse.objects.all()
    university = University.objects.all()
    if request.method == 'GET':
        formeset = RemotecourseModelFormset(
            queryset=RemoteCourse.objects.none())
        universityOnly = UniversityOnlyForm()
        seasonAndYear = seasonAndYearForm()
    if request.method == 'POST':
        current_user = request.user.userinfo
        formeset = RemotecourseModelFormset(request.POST)
        universityOnly = UniversityOnlyForm(request.POST or None)
        seasonAndYear = seasonAndYearForm(request.POST or None)
        try:
            c = CourseMap.objects.get(UserInfo = current_user)
            messages.error(
                        request, 'Cant input more than one Course Map!')
            # print("Course Map already exists")
        except:
            if formeset.is_valid() and universityOnly.is_valid():
                print("formeset Validated!")
                remote_courses = []
                university_in_forms = universityOnly.cleaned_data.get('University')
                department_name = current_user.department
                department = Department.objects.get(fullname = department_name)
                #university_in_forms = University.objects.get(id = university_in_forms_code)
                UserInfo_in_forms = "None"
                for form in formeset:
                    form_userinfo = request.user.userinfo
                    #university = form.cleaned_data.get('university')
                    code = form.cleaned_data.get('code')
                    name = form.cleaned_data.get('name')
                    #department = form.cleaned_data.get('department')
                    homecourse = form.cleaned_data.get('homecourse')
                    #season = form.cleaned_data.get('season')
                    #year = form.cleaned_data.get('year')
                    UserInfo_in_forms = form_userinfo
                    #university_in_forms = university
                    remotecourse = RemoteCourse(UserInfo=form_userinfo, university=university_in_forms, code=code,
                                                name=name,homecourse=homecourse)
                    remotecourse.save()
                    remote_courses.append(remotecourse)
                #instance = CourseMap.objects.create(UserInfo = UserInfo_in_forms,University = university_in_forms,department = department_in_forms)
                instance = CourseMap.objects.create(
                    UserInfo=UserInfo_in_forms, University=university_in_forms,department=department)
                instance.remote_courses.set(remote_courses)
                print("Instance has been saved")
                instance.save()
                return redirect('main:mapper_home')
    return render(request, template_name, {
        'formset': formeset,
        # 'heading': current_name,
        'result':result,
        'university':university,
        'uni_only': universityOnly,
        'season_only': seasonAndYear
    })


# Blog Views Below

def blog(request):
    exp = []
    form = SearchForm(request.POST or None)
    uni_in_query = request.GET.get('university_search')
    exp = Expierence.objects.all()
    if uni_in_query != '' and uni_in_query is not None:
        exp = []
        # print(uni_in_query)
        c = CourseMap.objects.filter(
            University__fullname__icontains=uni_in_query)
        for x in c:
            if Expierence.objects.get(UserInfo=x.UserInfo) is not None:
                exp.append(Expierence.objects.get(UserInfo=x.UserInfo))
        if len(exp) == 0:
            exp = []
    if uni_in_query == '':
        exp = Expierence.objects.all()
    """
    if request.method == 'GET':
        exp = Expierence.objects.all()
    """
    passon = {
        'Exp': exp,
        'form': form
    }
    return render(request, 'main/blog.html', passon)


@method_decorator(login_required, name='dispatch')
class BlogListView(ListView):
    model = Expierence
    template_name = 'main/blog.html'
    form_class = SearchForm
    # context_object_name = 'Exp'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Exp'] = Expierence.objects.all()
        context['active_search'] = 'current'
        return context

# @method_decorator(login_required, name='dispatch')
# class BlogDetailView(DetailView):
#     model = Expierence
#     template_name = 'main/experience.html'
#     context_object_name = 'data'


@login_required
def blog_detail_view(request, pk):
    context = {}
    context['exp'] = Expierence.objects.get(pk=pk)
    context['comment'] = Comment.objects.filter(experience=context['exp'])
    context['is_verified'] = context['exp'].is_verified
    user = context['exp'].UserInfo
    course_map_of_user = CourseMap.objects.get(UserInfo=user)
    context['uni'] = course_map_of_user.University
    """
    if request.method == 'GET':
        form = CommentForm(None)
    """
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data.get('comment')
            writer = UserInfo.objects.get(user=request.user)
            comment = Comment(
                experience=context['exp'], writer=writer, text=comment_text)
            comment.save()
            form = CommentForm()
    else:
        form = CommentForm()
    context['form'] = form
    return render(request, 'main/experience.html', context)


@login_required
def experienceform(request):
    if request.method == 'POST':
        userinfo = UserInfo.objects.get(user=request.user)
        try:
            c = CourseMap.objects.get(UserInfo=userinfo)
            form = ExperienceForm(request.POST, request.FILES)
            if form.is_valid():
                userinfo = UserInfo.objects.get(user=request.user)
                experience = Expierence(UserInfo=userinfo, para1=form.cleaned_data['para1'], para2=form.cleaned_data['para2'], para3=form.cleaned_data[
                                        'para3'], img1=form.cleaned_data['img1'], img2=form.cleaned_data['img2'], img3=form.cleaned_data['img3'], iframe=form.cleaned_data['iframe'])
                try:
                    # print(2)
                    experience.save()
                    return redirect('main:blog')
                except:
                    # print(3)
                    messages.error(
                        request, 'Cant fill more than one experience')
                    # redirect('main:blog')
            else:
                # print(4)
                print("There was some problem...")
        except CourseMap.DoesNotExist:
            c = None
            form = ExperienceForm()
            messages.error(request, 'You need to add a course map first')
            redirect('main:blog')
    else:
        form = ExperienceForm()

    return render(request, 'main/experience_form.html', {'form': form})


""""
@login_required
def addUniversity(request):
    if request.method == 'POST':
        form = UniversityForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data.get('fullname')
            city = form.cleaned_data.get('city')
            country = form.cleaned_data.get('country')
            university = University(
                fullname=fullname, city=city, country=country)
            university.save()
            return redirect('main:your_exp')
    else:
        form = UniversityForm()
    return render(request, "main/add_uni.html", {'form': form})
"""


@login_required
def query_view(request):
    list_doubt = Doubt.objects.annotate(
        no_of_answer=Count('answer')).order_by('-no_of_answer')
    return render(request, 'main/query-form.html', {'list_doubt': list_doubt})


@login_required
def doubt_form_view(request):
    if request.method == 'POST':
        form = DoubtForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            student = UserInfo.objects.get(user=request.user)
            doubt = Doubt(student=student, text=text)
            doubt.save()
            return redirect('main:doubt')
    else:
        form = DoubtForm()
    return render(request, 'main/query-form-page.html', {'form': form})


@login_required
def answer_view(request, pk):
    doubt = Doubt.objects.get(pk=pk)
    list_answer = Answer.objects.filter(doubt=doubt).order_by('-upvote')
    return render(request, 'main/answer.html', {'list_answer': list_answer, 'doubt': doubt})


@login_required
def answer_view_form(request, id):
    doubt = Doubt.objects.get(pk=id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            anonymous = form.cleaned_data.get('anonymous')
            answer = Answer(text=text, doubt=doubt)
            if not anonymous:
                author = UserInfo.objects.get(user=request.user)
                answer.author = author
            answer.save()
            return redirect('main:answer' , pk=str(id))
    else:
        form = AnswerForm()
    return render(request, 'main/answer-form-page.html', {'form': form, 'doubt': doubt})


@login_required
def upvote_view(request, pk, id):
    answer = Answer.objects.get(pk=pk)
    voter = UserInfo.objects.get(user=request.user)
    if voter.upvoted.filter(pk=pk).exists():
        answer.upvote -= 1
        voter.upvoted.remove(answer)
        answer.save()
        voter.save()
    elif voter.downvoted.filter(pk=pk).exists():
        answer.downvote -= 1
        voter.downvoted.remove(answer)
        answer.upvote += 1
        voter.upvoted.add(answer)
        answer.save()
        voter.save()
    else:
        answer.upvote += 1
        voter.upvoted.add(answer)
        answer.save()
        voter.save()
    return redirect('main:answer' , pk=str(id))


@login_required
def downvote_view(request, pk, id):
    answer = Answer.objects.get(pk=pk)
    voter = UserInfo.objects.get(user=request.user)
    if voter.downvoted.filter(pk=pk).exists():
        answer.downvote -= 1
        voter.downvoted.remove(answer)
        answer.save()
        voter.save()
    elif voter.upvoted.filter(pk=pk).exists():
        answer.upvote -= 1
        voter.upvoted.remove(answer)
        answer.downvote += 1
        voter.downvoted.add(answer)
        answer.save()
        voter.save()
    else:
        answer.downvote += 1
        voter.downvoted.add(answer)
        answer.save()
        voter.save()
    return redirect('main:answer' , pk=str(id))

# Adding custom error views


def error_404(request, exception):
    return render(request, 'main/error.html', {'error': '404', 'error_text': 'Ooops!!! The page you are looking for is not found'})


def error_500(request, *args, **argv):
    return render(request, 'main/error.html', {'error': '500', 'error_text': '500 Internal Server Error'})


def error_403(request,  exception):
    return render(request, 'main/error.html', {'error': '403', 'error_text': 'Forbidden Error'})


def error_400(request,  exception):
    return render(request, 'main/error.html', {'error': '400', 'error_text':  'Bad Request'})


# @login_required
# def yourExperience(request):
#     univlist = University.objects.all()
#     if request.method == 'POST':
#         form = UniversityInputForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['fullname']
#             id = len(University.objects.all()) + 1
#             univ = University(fullname = name, id = id)
#             univ.save()
#     else:
#         form = UniversityInputForm()
#     return render(request, 'main/your_exp.html', {'form':form, 'univlist':univlist})

"""
        form = InputForm(request.POST or None)
        university_id = request.GET.get('University')
        semester_code = request.GET.get('semester')
        year = request.GET.get('year')
        department = "Department"
        if request.GET.get('department'):
            department = request.GET.get('department')
        #print(university_id + " " + department)
        exp = CourseMap.objects.all() #Without filter data
        exp = exp.filter(is_verified = True)#Verification filter
        if university_id != 'None' and university_id is not None:
            university_in_query = University.objects.filter(id = university_id)
            exp = exp.filter(University__in = university_in_query) #in was important here
        
        if department != 'Department' and department is not None:
            exp = exp.filter(UserInfo__department__icontains = department) #in was important here
        
        if year != 'None' and year is not None:
            #year=2 is what we recieve
            all_remote_courses = RemoteCourse.objects.filter(homecourse__year__in = year)
            exp = exp.filter(remote_courses__in = all_remote_courses).distinct()#distinct() returns only one filter here

        if semester_code != 'None' and semester_code is not None:
            #semester=S is what we recieve means spring
            all_remote_courses = RemoteCourse.objects.filter(homecourse__season__in = semester_code)
            exp = exp.filter(remote_courses__in = all_remote_courses).distinct()
        passon = {
            'p':exp,
        }
        return render(request,"main/form.html",{'form':form,'passon':passon})
"""
"""
class FilterResultsView(ListView):
 Render search results.
    model= RemoteCourse
    template_name= "main/form.html"


    def get_queryset(self, **kwargs):
        if 'code_letters' not in self.request.GET:
            return None
        return Course.objects.filter(department__code__icontains= self.request.GET.get('code_letters')).filter(code__icontains= self.request.GET.get('code_digits')).order_by('code')


    def get_context_data(self, **kwargs):
        context = super(FilterResultsView, self).get_context_data(**kwargs)
        context['form'] = SearchCoursesForm(auto_id= False)
        context['active_search'] = 'current'
        return context
"""
