from django.db import models
from wikinotes.models.semesters import Semester
from wikinotes.models.courses import Course
from wikinotes.utils.pages import get_possible_exams
from wikinotes.utils.semesters import get_possible_years, get_possible_terms

# The "base" page class - all specific page types have a one-to-one relationship with this
class Page(models.Model):
	class Meta:
		app_label = 'wikinotes'
		
	course = models.ForeignKey(Course)
	# Determines how many files are needed. Always user-configurable, even for vocab quizzes
	num_sections = models.IntegerField()

# Oh fuck this is so awesome
class LectureNote(Page):
	class Meta:
		app_label = 'wikinotes'
		
	semester = models.ForeignKey(Semester)
	lecture_num = models.IntegerField()
	subject = models.CharField(max_length=100)
	date = models.DateField()
	
	# Stuff that will need to be displayed for all pages etc
	def __unicode__(self):
		return "Lecture %d (%s)" % (self.lecture_num, self.subject)
	
	# The slug thing ... the URI basically but whatever URL works
	def get_url(self):
		return "lecture/%s-%d/%d" % (self.semester.term, self.semester.year, self.lecture_num)
	
class PastExam(Page):
	class Meta:
		app_label = 'wikinotes'
		
	# Exam types: final, midterm and that's all for now lol
	exam_type = models.CharField(max_length=10, choices=get_possible_exams())
	# Doesn't have an associated semester
	# See if it's possible to move semester = ForeignKey into Page and just override it here
	semester = None
	# The term and year when the exam was written
	term = models.CharField(max_length=6, choices=get_possible_terms())
	year = models.IntegerField(max_length=4, choices=get_possible_years())
	
	# Display as: Winter 2008 final exam or Fall 2009 midterm exam
	def __unicode__(self):
		return "%s %s %s exam" % (self.term, self.year, self.exam_type)
	
	def get_url(self):
		return "exam/%s-%s-%s" % (self.term, self.year, self.exam_type)

class CourseQuiz(Page):
	class Meta:
		app_label = 'wikinotes'
		
	semester = models.ForeignKey(Semester)
	subject = models.CharField(max_length=100)
	
	def __unicode__(self):
		return "%s (course quiz)" % self.subject
	
	def get_url(self):
		# First make the subject URL-friendly
		return "course-quiz/"

# The difference between course and vocab quizzes:
# For course quizzes, you have a question, and several MC answers (like my lab practice final)
# For vocab quizzes, you just match shit (like terms, definitions etc)
class VocabQuiz(Page):
	class Meta:
		app_label = 'wikinotes'
		
	semester = models.ForeignKey(Semester)
	subject = models.CharField(max_length=100)
	
	def __unicode__(self):
		return "%s (vocabulary quiz)" % self.subject

# Includes miscellaneous shit too
class CourseSummary(Page):
	class Meta:
		app_label = 'wikinotes'
		
	semester = models.ForeignKey(Semester)
	subject = models.CharField(max_length=100)
	
	def __unicode__(self):
		return "%s (course summary)" % self.subject