from django.shortcuts import render_to_response, get_object_or_404
from wiki.models.courses import Course, CourseSemester
from wiki.models.faculties import Faculty
from wiki.models.departments import Department
from utils import page_types as types
from django.template import RequestContext
from wiki.models.pages import Page

# Faculty no longer looks like a word to me
def faculty(request):
	faculty_objects = Faculty.objects.all().order_by('name')
	courses = Course.objects.all()
	faculties = []

	for faculty in faculty_objects:
		faculty_courses = courses.filter(department__faculty=faculty).order_by('department__short_name', 'number')
		faculties.append({'name': faculty.name, 'slug': faculty.slug, 'courses': faculty_courses})

	data = {
		'faculties': faculties,
	}

	return render_to_response('courses/faculty.html', data)

# Same pattern as faculty view
def department(request):
	department_objects = Department.objects.all().order_by('long_name')
	courses = Course.objects.all()
	departments = []

	for department in department_objects:
		department_courses = courses.filter(department=department).order_by('department__short_name', 'number')
		departments.append({'long': department.long_name, 'short': department.short_name, 'courses': department_courses})

	data = {
		'departments': departments,
	}

	return render_to_response('courses/department.html', data)

# Not really sure how to best implement this lol
def semester(request):
	return render_to_response('courses/semester.html')

# Meh
def professor(request):
	return render_to_response('courses/professor.html')

def index(request):
	return render_to_response('courses/index.html')

def all(request):
	courses = Course.objects.all().order_by('department', 'number')
	data = {
		'courses': courses,
	}
	return render_to_response('courses/all.html', data)

def overview(request, department, number):
	course = get_object_or_404(Course, department=department, number=int(number))

	# We can't use it directly in the template file, it just won't work
	page_types = []
	for name, obj in types.iteritems():
		# Get all the pages associated with this page type (and this course etc)
		pages = Page.objects.filter(page_type=name, course_sem__course=course)
		page_types.append({'name': name, 'url': obj.get_create_url(course), 'icon': obj.get_icon(), 'long_name': obj.long_name, 'desc': obj.description, 'show_template': obj.get_show_template(), 'list_template': obj.get_list_template(), 'pages': pages})

	try:
		this_sem = CourseSemester.objects.get(course=course, term='winter', year='2011')
		this_sem_pages = this_sem.page_set.all()
	except CourseSemester.DoesNotExist:
		this_sem_pages = []

	# Get all the course semesters related to this course
	course_sems = CourseSemester.objects.filter(course=course)
	data = {
		'course': course,
		'page_types': page_types,
		'this_sem_pages': this_sem_pages,
		'course_sems': course_sems,
	}
	return render_to_response('courses/overview.html', data)