from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Admin, Course, Feedback, List, Student, Question, StudentResponse, Grades, OTP, TotalPercentage
import json, random
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
import random
import string
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Max
from django.utils import timezone
from django.db.models import Count
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.safestring import mark_safe
import os
from urllib.parse import urljoin

def generate_student_id(request):
    current_year = datetime.now().year
    while True:
        random_id = random.randint(1000, 9999)
        student_id = int(f"{current_year}{random_id}")
        if not Student.objects.filter(StudentID=student_id).exists():
            break

    request.session['student_id'] = student_id

    student = Student(StudentID=student_id, Year=current_year)
    student.save()

    return JsonResponse({'student_id': student_id})

def loginForm(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Admin.objects.get(Email=email)

            if check_password(password, user.Password):
                request.session['user_role'] = user.Role
                if user.Role == 'Teacher':
                    request.session['teacher_email'] = user.Email
                    request.session['teacher_course'] = user.Course
                    request.session['teacher_id'] = user.id
                    request.session['teacher_role'] = user.Role

                if user.Role == 'Admin':
                    request.session['user_id'] = user.id
                    request.session['user_role'] = user.Role
                    request.session['user_email'] = user.Email
                    return redirect('dashboardAdmin')
                elif user.Role == 'Teacher':
                    return redirect('dashboardTeacher')
                else:
                    messages.error(request, 'Role not recognized.')
            else:
                messages.error(request, 'Invalid email or password.')

        except Admin.DoesNotExist:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'studentPanel/loginForm.html')

def course(request):
    if not request.session.get('user_id'):
        return redirect('loginForm')

    if not request.session.get('user_role') == 'Admin':
        return redirect('loginForm')

    course_id = request.GET.get('view', None)
    editing_id = request.GET.get('edit', None)
    selected_college = request.GET.get('college', '')

    courses = Course.objects.all()
    colleges = Course.objects.values_list('College', flat=True).distinct()

    if selected_college:
        courses = courses.filter(College=selected_college)

    if course_id:
        course = get_object_or_404(Course, id=course_id)
        return render(request, 'adminPanel/courses.html', {'course': course, 'colleges': colleges})

    if editing_id:
        course = get_object_or_404(Course, id=editing_id)
        if request.method == 'POST':
            course.College = request.POST.get('College', course.College)
            course.Course = request.POST.get('Course', course.Course)
            course.AvgGrade = request.POST.get('AvgGrade', course.AvgGrade)
            course.AvgCet = request.POST.get('AvgCet', course.AvgCet)
            course.TotalScore = request.POST.get('AvgCet', course.AvgCet)
            course.CourseDescription = request.POST.get('CourseDescription', course.CourseDescription)
            course.save()
            return redirect('course')

        return render(request, 'adminPanel/courses.html', {'course': course, 'editing': True, 'colleges': colleges})

    return render(request, 'adminPanel/courses.html', {
        'courses': courses,
        'colleges': colleges,
    })

def teacherCourses(request):
    if not request.session.get('teacher_id'):
        return redirect('loginForm')

    if not request.session.get('teacher_role') == 'Teacher':
        return redirect('login')

    teacher_course = request.session.get('teacher_course', None)

    if not teacher_course:
        return render(request, 'teacherPanel/teacherCourses.html', {
            'error': 'No course assigned to this teacher.',
        })

    course_id = request.GET.get('view', None)
    editing_id = request.GET.get('edit', None)
    selected_college = request.GET.get('college', '')

    courses = Course.objects.filter(Course=teacher_course)
    colleges = courses.values_list('College', flat=True).distinct()

    if course_id:
        course = get_object_or_404(courses, id=course_id)
        return render(request, 'teacherPanel/teacherCourses.html', {
            'course': course,
            'colleges': colleges
        })

    if editing_id:
        course = get_object_or_404(courses, id=editing_id)
        if request.method == 'POST':
            course.College = request.POST.get('College', course.College)
            course.Course = request.POST.get('Course', course.Course)
            course.AvgGrade = request.POST.get('AvgGrade', course.AvgGrade)
            course.AvgCet = request.POST.get('AvgCet', course.AvgCet)
            course.TotalScore = request.POST.get('TotalScore', course.TotalScore)
            course.CourseDescription = request.POST.get('CourseDescription', course.CourseDescription)
            course.save()
            return redirect('teacherCourses')

        return render(request, 'teacherPanel/teacherCourses.html', {
            'course': course,
            'editing': True,
            'colleges': colleges
        })

    return render(request, 'teacherPanel/teacherCourses.html', {
        'courses': courses,
        'teacher_course': teacher_course,
        'colleges': colleges
    })

def teacherPanel(request):
    # Check if teacher is logged in
    if not request.session.get('teacher_id'):
        return redirect('loginForm')

    # Ensure correct role
    if request.session.get('teacher_role') != 'Teacher':
        return redirect('login')

    # Retrieve teacher details from session
    teacher_email = request.session.get('teacher_email')
    teacher_course = request.session.get('teacher_course')

    print(f"Teacher's Course from Session: {teacher_course}")

    selected_course = request.GET.get('course', '')
    search_query = request.GET.get('search', '')

    current_year = datetime.now().year
    students = List.objects.filter(Status='Pending', Course=teacher_course, Year=current_year)

    print(f"Initial Student Count: {students.count()}")

    if selected_course:
        students = students.filter(Course=selected_course)
        print(f"After Filtering by Selected Course: {selected_course}, Count: {students.count()}")

    if search_query:
        students = students.filter(Name__icontains=search_query)
        print(f"After Filtering by Search Query: {search_query}, Count: {students.count()}")

    students = students.order_by('-AvgCet')

    print(f"Final Student Count: {students.count()}")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        student_list = list(students.values(
            'id', 'Name', 'Email', 'AvgGrade', 'AvgCet', 'Number', 'ApplicationNo',
            'Address', 'Course', 'EnglishProficiency', 'ReadingComprehension',
            'ScienceProcessSkills', 'MathematicalSkills', 'AbstractLogicThinkingSkills', 'CetPicture', 'GradePicture',
        ))
        return JsonResponse({'students': student_list})

    return render(request, 'teacherPanel/teacherPanel.html', {
        'students': students,
        'teacher_course': teacher_course,  # Pass teacher's course to the template
        'selected_course': selected_course,
        'search_query': search_query,
    })

def feedback(request):
    if not request.session.get('user_id'):
        return redirect('loginForm')

    if not request.session.get('user_role') == 'Admin':
        return redirect('loginForm')

    feedbacks = Feedback.objects.all()
    return render(request, 'adminPanel/feedback.html', {'feedbacks': feedbacks})

def get_grouped_questions():
    from collections import defaultdict

    grouped = defaultdict(set)
    questions = Question.objects.all()

    for question in questions:
        grouped[question.text].add(question.courseName)

    grouped_questions = [{'text': text, 'courses': list(courses)} for text, courses in grouped.items()]

    return grouped_questions

def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    if request.method == 'POST':
        if 'name' in request.POST and 'feedback' in request.POST:
            name = request.POST.get('name')
            feedback = request.POST.get('feedback')
            Feedback.objects.create(Name=name, Feedback=feedback)
            return JsonResponse({'message': 'Feedback submitted successfully'})

        if 'studentID' in request.POST:
            student_id = request.POST.get('studentID')
            avg_grade = request.POST.get('avg_grade')
            avg_cet = request.POST.get('avg_cet')

            avg_grade = float(avg_grade) if avg_grade else 0
            avg_cet = float(avg_cet) if avg_cet else 0

            question_texts = [key for key in request.POST.keys() if key.startswith('questions_')]

            for q in question_texts:
                question_text = request.POST.get(q)
                response_key = f"response_{q.split('_')[-1]}"
                response_value = request.POST.get(response_key)

                if response_value:
                    courses = Question.objects.filter(text=question_text).values_list('courseName', flat=True).distinct()

                    for course in courses:
                        StudentResponse.objects.create(
                            StudentID=student_id,
                            question=question_text,
                            response=float(response_value),
                            courseName=course
                        )

            save_grades(student_id, avg_grade, avg_cet)

            context = {
                'questions': get_grouped_questions(),
                'success_message': 'Responses and grades submitted successfully!'
            }
            return render(request, 'studentPanel/dashboard.html', context)

    context = {
        'questions': get_grouped_questions()
    }

    return render(request, 'studentPanel/dashboard.html', context)

from django.db.models import Avg, Sum

def compute_personality_score(student_id, course_name):
    responses = StudentResponse.objects.filter(StudentID=student_id, courseName=course_name)

    if not responses.exists():
        return 0

    personality_score = 0

    for response in responses:
        question = Question.objects.filter(text=response.question, courseName=course_name).first()

        if question and question.Percentage:
            percentage = question.Percentage
        else:
            percentage = 0

        personality_score = response.response * percentage

    return personality_score

def compute_total_score(avg_grade, personality_score, avg_cet):
    percentages = TotalPercentage.objects.first()
    if not percentages:
        cet_percentage = 0.4
        grade_percentage = 0.3
        personality_percentage = 0.3
    else:
        cet_percentage = percentages.CetAvgPercentage
        grade_percentage = percentages.GradeAvgPercentage
        personality_percentage = percentages.PersonalityPercentage

    return (
        (grade_percentage * avg_grade) +
        (personality_percentage * personality_score) +
        (cet_percentage * avg_cet)
    )

from django.contrib import messages

def adminSetting(request):
    if not request.session.get('user_id'):
        return redirect('loginForm')

    if not request.session.get('user_role') == 'Admin':
        return redirect('loginForm')

    if request.method == "POST":
        if "change_password" in request.POST:
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            admin_email = request.session.get('user_email')

            try:
                admin = Admin.objects.get(Email=admin_email)
                if check_password(old_password, admin.Password):
                    admin.Password = make_password(new_password)
                    admin.save()
                    messages.success(request, "Password changed successfully!")
                else:
                    messages.error(request, "Old password is incorrect.")
            except Admin.DoesNotExist:
                messages.error(request, "Admin not found.")

        elif "update_percentage" in request.POST:
            cet_percentage = float(request.POST.get("cet_percentage", 0))
            grade_percentage = float(request.POST.get("grade_percentage", 0))
            personality_percentage = float(request.POST.get("personality_percentage", 0))

            total_percentage = cet_percentage + grade_percentage + personality_percentage
            if total_percentage != 1.0:
                messages.error(request, "The total percentage must be equal to 100%. Please adjust the values.")
            else:
                total_percentage, created = TotalPercentage.objects.get_or_create(id=1)
                total_percentage.CetAvgPercentage = cet_percentage
                total_percentage.GradeAvgPercentage = grade_percentage
                total_percentage.PersonalityPercentage = personality_percentage
                total_percentage.save()
                messages.success(request, "Percentages updated successfully!")

    total_percentage = TotalPercentage.objects.first()
    context = {
        "cet_percentage": total_percentage.CetAvgPercentage if total_percentage else 0,
        "grade_percentage": total_percentage.GradeAvgPercentage if total_percentage else 0,
        "personality_percentage": total_percentage.PersonalityPercentage if total_percentage else 0,
        "messages": messages.get_messages(request),  # Pass messages to the template
    }
    return render(request, "adminPanel/setting.html", context)

def save_grades(student_id, avg_grade=None, avg_cet=None):
    questions = StudentResponse.objects.filter(StudentID=student_id).values_list('question', flat=True).distinct()

    for question_text in questions:
        courses = Question.objects.filter(text=question_text).values_list('courseName', flat=True).distinct()

        for course_name in courses:
            response = StudentResponse.objects.filter(StudentID=student_id, question=question_text, courseName=course_name).first()

            if not response:
                continue

            question_data = Question.objects.filter(text=question_text, courseName=course_name).first()
            percentage = question_data.Percentage if question_data and hasattr(question_data, 'Percentage') else 0
            category = question_data.Category if question_data and hasattr(question_data, 'Category') else 0  # ✅ Get Category

            personality_score = response.response * percentage

            avg_grade_input = avg_grade if avg_grade is not None else response.response
            avg_cet_input = avg_cet if avg_cet is not None else response.response

            total_score = compute_total_score(avg_grade_input, personality_score, avg_cet_input)

            # Save record with the question and category included
            Grades.objects.create(
                StudentID=student_id,
                courseName=course_name,
                AvgGrade=avg_grade_input,
                AvgCet=avg_cet_input,
                TotalScore=total_score,
                PersonalityScore=personality_score,
                Question=question_text,  # Store the question text
                Category=category  # ✅ Store Category
            )
from django.db.models import Max
import json
import logging
from django.shortcuts import render, redirect

def recommend_courses(request, student_id):
    if not request.session.get('student_id'):
        return redirect('loginForm')

    try:
        # Fetch grades only with required fields, ordered by highest TotalScore
        grades = Grades.objects.filter(StudentID=student_id).only(
            "StudentID", "TotalScore", "AvgGrade", "AvgCet", "courseName"
        ).order_by('-TotalScore')

        if not grades.exists():
            return render(request, 'studentPanel/recommendation.html', {
                'error': 'No grades available for recommendations.',
                'student_id': student_id
            })

        # Fetch all courses and map by name for fast lookup
        all_courses = Course.objects.values(
            "Course", "AvgGrade", "AvgCet", "Category", "College", "CourseDescription", "Logo", "reason", "MainLogo"
        )
        course_dict = {course["Course"].strip().lower(): course for course in all_courses}

        # Find highest TotalScore for each category
        category_scores = {}
        for g in grades:
            course_name = g.courseName.strip().lower()
            if course_name in course_dict:
                category = course_dict[course_name]["Category"]
                category_scores[category] = max(category_scores.get(category, 0), g.TotalScore)

        if not category_scores:
            return render(request, 'studentPanel/recommendation.html', {
                'error': 'No matching course categories found for recommendations.',
                'student_id': student_id
            })

        # Determine the highest TotalScore
        highest_score = max(category_scores.values())

        # Find all categories that share this highest score
        highest_categories = [category for category, score in category_scores.items() if score == highest_score]

        # Fetch only courses from the highest categories
        filtered_courses = Course.objects.filter(Category__in=highest_categories).values(
            "Course", "AvgGrade", "AvgCet", "Category", "College", "CourseDescription", "Logo", "reason", "MainLogo"
        )

        # Match courses with grades and recommend if criteria match
        recommended_courses = []
        for course in filtered_courses:
            corresponding_grade = next((g for g in grades if g.courseName.strip().lower() == course["Course"].strip().lower()), None)
            if corresponding_grade and corresponding_grade.AvgGrade >= course["AvgGrade"] and corresponding_grade.AvgCet >= course["AvgCet"]:
                recommended_courses.append({
                    **course,
                    'TotalScore': corresponding_grade.TotalScore,
                    'PersonalityScore': corresponding_grade.PersonalityScore,
                })

        # Sort by TotalScore and recommend top 6
        recommended_courses = sorted(recommended_courses, key=lambda x: x['TotalScore'], reverse=True)[:6]

        # Graph Data for Courses
        course_graph_data = list(
            Grades.objects.filter(StudentID=student_id)
            .exclude(courseName__isnull=True)
            .exclude(courseName="")
            .values("courseName")
            .annotate(MaxTotalScore=Max("TotalScore"))
            .order_by("courseName")
        )

        # Graph Data for Questions
        question_graph_data = list(
            Grades.objects.filter(StudentID=student_id)
            .exclude(Question__isnull=True)
            .exclude(Question="")
            .values("Question")
            .annotate(MaxTotalScore=Max("TotalScore"))
            .order_by("Question")
        )

        return render(request, 'studentPanel/recommendation.html', {
            'courses': recommended_courses,
            'student_id': student_id,
            'course_graph_data': json.dumps(course_graph_data),
            'question_graph_data': json.dumps(question_graph_data)
        })

    except Exception as e:
        logging.error(f'Error in recommend_courses: {str(e)}')
        return render(request, 'studentPanel/recommendation.html', {
            'error': f'Internal Server Error: {str(e)}',
            'student_id': student_id
        })

# from django.db.models import Max
# import json
# import logging

# def recommend_courses(request, student_id):
#     if not request.session.get('student_id'):
#         return redirect('loginForm')

#     try:
#         grades = list(Grades.objects.filter(StudentID=student_id).order_by('-TotalScore'))

#         if not grades:
#             return render(request, 'studentPanel/recommendation.html', {
#                 'error': 'No grades available for recommendations.',
#                 'student_id': student_id
#             })

#         all_courses = list(Course.objects.all())
#         course_dict = {course.Course.strip().lower(): course for course in all_courses}

#         highest_total_score = grades[0].TotalScore
#         categories = {course_dict[g.courseName.strip().lower()].Category for g in grades if g.courseName.strip().lower() in course_dict}

#         recommended_courses = []
#         for course in all_courses:
#             if course.Category in categories:
#                 corresponding_grade = next((g for g in grades if g.courseName.strip().lower() == course.Course.strip().lower()), None)
#                 if corresponding_grade and corresponding_grade.AvgGrade >= course.AvgGrade and corresponding_grade.AvgCet >= course.AvgCet:
#                     recommended_courses.append({
#                         'Course': course.Course,
#                         'AvgGrade': course.AvgGrade,
#                         'AvgCet': course.AvgCet,
#                         'TotalScore': corresponding_grade.TotalScore,
#                         'PersonalityScore': corresponding_grade.PersonalityScore,
#                         'College': course.College,
#                         'CourseDescription': course.CourseDescription,
#                         'Logo': course.Logo,
#                         'reason': course.reason,
#                         'Category': course.Category,
#                         'MainLogo': course.MainLogo,
#                     })

#         recommended_courses = sorted(recommended_courses, key=lambda x: x['TotalScore'], reverse=True)[:8]  # Limit to top 8

#         # Graph Data for Courses
#         course_graph_data = [
#             {"courseName": entry["courseName"] or "Unknown Course", "MaxTotalScore": entry["MaxTotalScore"]}
#             for entry in Grades.objects.filter(StudentID=student_id)
#             .exclude(courseName__isnull=True)
#             .exclude(courseName="")
#             .values("courseName")
#             .annotate(MaxTotalScore=Max("TotalScore"))
#             .order_by("courseName")
#         ]

#         # Graph Data for Questions
#         question_graph_data = [
#             {"Question": entry["Question"] or "Unknown Question", "MaxTotalScore": entry["MaxTotalScore"]}
#             for entry in Grades.objects.filter(StudentID=student_id)
#             .exclude(Question__isnull=True)
#             .exclude(Question="")
#             .values("Question")
#             .annotate(MaxTotalScore=Max("TotalScore"))
#             .order_by("Question")
#         ]

#         return render(request, 'studentPanel/recommendation.html', {
#             'courses': recommended_courses,
#             'student_id': student_id,
#             'course_graph_data': json.dumps(course_graph_data),
#             'question_graph_data': json.dumps(question_graph_data)
#         })

#     except Exception as e:
#         logging.error(f'Error in recommend_courses: {str(e)}')
#         return render(request, 'studentPanel/recommendation.html', {
#             'error': f'Internal Server Error: {str(e)}',
#             'student_id': student_id
#         })

# import logging
# from django.db.models import Max

# def recommend_courses(request, student_id):
#     if not request.session.get('student_id'):
#         return redirect('loginForm')

#     try:
#         grades = Grades.objects.filter(StudentID=student_id).order_by('-TotalScore')

#         if not grades.exists():
#             return render(request, 'studentPanel/recommendation.html', {
#                 'error': 'No grades available for recommendations.',
#                 'student_id': student_id
#             })

#         all_courses = Course.objects.all()
#         highest_grade = grades.first()
#         highest_total_score = highest_grade.TotalScore
#         same_score_grades = grades.filter(TotalScore=highest_total_score)

#         categories = set()
#         for grade in same_score_grades:
#             course_key = grade.courseName.strip().lower()
#             highest_course = next((c for c in all_courses if c.Course.strip().lower() == course_key), None)
#             if highest_course:
#                 categories.add(highest_course.Category)

#         recommended_courses = []
#         for course in all_courses:
#             if course.Category in categories:
#                 corresponding_grade = grades.filter(courseName__iexact=course.Course).first()
#                 course_total_score = corresponding_grade.TotalScore if corresponding_grade else 0

#                 recommended_courses.append({
#                     'Course': course.Course,
#                     'AvgGrade': course.AvgGrade,
#                     'AvgCet': course.AvgCet,
#                     'TotalScore': course_total_score,
#                     'PersonalityScore': corresponding_grade.PersonalityScore if corresponding_grade else 0,
#                     'College': course.College,
#                     'CourseDescription': course.CourseDescription,
#                     'Logo': course.Logo,
#                     'reason': course.reason,
#                     'Category': course.Category,
#                 })

#         recommended_courses_sorted = sorted(recommended_courses, key=lambda x: x['TotalScore'], reverse=True)

#         # Graph Data Logic
#         graph_data = list(
#             Grades.objects.filter(StudentID=student_id)
#             .exclude(Question__isnull=True)  # Remove null questions
#             .exclude(Question="")  # Remove empty questions
#             .values("Question")
#             .annotate(MaxTotalScore=Max("TotalScore"))
#             .order_by("Question")
#         )

#         # Ensure graph data does not contain None values
#         for entry in graph_data:
#             entry["Question"] = entry["Question"] or "Unknown Question"

#         return render(request, 'studentPanel/recommendation.html', {
#             'courses': recommended_courses_sorted,
#             'student_id': student_id,
#             'graph_data': json.dumps(graph_data)  # Pass cleaned graph data to the template
#         })

#     except Exception as e:
#         logging.error(f'Error in recommend_courses: {str(e)}')
#         return render(request, 'studentPanel/recommendation.html', {
#             'error': f'Internal Server Error: {str(e)}',
#             'student_id': student_id
#         })

def exploreCourses(request):
    courses = Course.objects.all()
    colleges = courses.values_list('College', flat=True).distinct()

    if request.method == "POST":
        try:
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name', '')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            avg_grade = request.POST.get('avg_grade')
            avg_cet = request.POST.get('avg_cet')
            application_no = request.POST.get('ApplicationNo')
            contact_no = request.POST.get('contact_no')
            address = request.POST.get('address')
            course = request.POST.get('course')

            new_entry = List(
                Name=f"{first_name} {middle_name} {last_name}".strip(),
                Email=email,
                AvgGrade=avg_grade,
                AvgCet=avg_cet,
                Number=contact_no,
                ApplicationNo=application_no,
                Address=address,
                Course=course,
            )
            new_entry.save()

            return JsonResponse({'message': 'successfully add to the list, just wait for the approval of the teacher and keep checking your email!', 'status': 'success'})
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}', 'status': 'error'})

    return render(request, 'studentPanel/exploreCourses.html', {'courses': courses, 'colleges': colleges})

def result(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('loginForm')

    context = {
        'student_id': student_id,
    }
    return render(request, 'studentPanel/result.html', context)

@csrf_exempt
def add_to_list(request):
    year = datetime.now().year
    if request.method == 'POST':
        name = f"{request.POST.get('first_name')} {request.POST.get('middle_name', '')} {request.POST.get('last_name')}"
        email = request.POST.get('email')
        avg_grade = request.POST.get('avg_grade')
        avg_cet = request.POST.get('avg_cet')
        number = request.POST.get('contact_no')
        application_no = request.POST.get('ApplicationNo')
        address = request.POST.get('address')
        course = request.POST.get('course')
        # EngProfi = request.POST.get('EngProfi')
        # ReaCom = request.POST.get('ReaCom')
        # SciProSkil = request.POST.get('SciProSkil')
        # MatSkil = request.POST.get('MatSkil')
        # AbsLogThiSkil = request.POST.get('AbsLogThiSkil')

        cet_picture = request.FILES.get('cet_picture')
        grade_picture = request.FILES.get('grade_picture')

        new_entry = List(
            Name=name,
            Email=email,
            AvgGrade=avg_grade,
            AvgCet=avg_cet,
            Number=number,
            ApplicationNo=application_no,
            Address=address,
            Course=course,
            Year=year,
            # EnglishProficiency=EngProfi,
            # ReadingComprehension=ReaCom,
            # ScienceProcessSkills=SciProSkil,
            # MathematicalSkills=MatSkil,
            # AbstractLogicThinkingSkills=AbsLogThiSkil,
        )

        # Save entry first to get an ID for file naming
        new_entry.save()

        # Save images to the correct location
        if cet_picture:
            cet_path = f"{cet_picture.name}"
            new_entry.CetPicture.save(cet_path, cet_picture)

        if grade_picture:
            grade_path = f"{grade_picture.name}"
            new_entry.GradePicture.save(grade_path, grade_picture)

        new_entry.save()

        return JsonResponse({
            'message': 'Successfully added to the list!',
            'cet_picture': new_entry.CetPicture.url if new_entry.CetPicture else None,
            'grade_picture': new_entry.GradePicture.url if new_entry.GradePicture else None,
        })

    return JsonResponse({'message': 'Invalid request'}, status=400)

@csrf_exempt
def update_student_status(request):
    email = request.session.get('teacher_email')
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('id')
        status = data.get('status')

        try:
            student = List.objects.get(id=student_id)

            from_email = email

            subject = 'Your application Status Update'
            message = (
                f'Hello {student.Name},\n\n'
                f'Your application for {student.Course} status has been updated to: {status}.\n\n'
                f'Best regards,\nWestern Mindanao State University'
            )
            recipient_list = [student.Email]

            try:
                send_mail(subject, message, from_email, recipient_list)
            except BadHeaderError:
                return JsonResponse({'message': 'Failed to send email due to an invalid header.'}, status=400)
            except Exception as e:
                return JsonResponse({'message': f'Failed to send email. Please check your connection and try again. {str(e)}'}, status=500)

            student.Status = status
            student.Year = datetime.now().year
            student.save()

            return JsonResponse({'message': 'Status updated and email sent successfully!'})

        except List.DoesNotExist:
            return JsonResponse({'message': 'Student not found.'}, status=404)

    return JsonResponse({'message': 'Invalid request.'}, status=400)

from datetime import datetime
from django.db.models import Max
from datetime import datetime

def approved_students(request):
    if not request.session.get('teacher_id'):
        return redirect('loginForm')

    if not request.session.get('teacher_role') == 'Teacher':
        return redirect('login')

    teacher_email = request.session.get('teacher_email', None)

    if not teacher_email:
        return render(request, 'teacherPanel/teacherCourses.html', {
            'error': 'No teacher logged in.',
        })

    try:
        teacher = Admin.objects.get(Email=teacher_email)
        teacher_course = teacher.Course
    except Admin.DoesNotExist:
        return render(request, 'teacherPanel/teacherCourses.html', {
            'error': 'Teacher not found.',
        })

    search_query = request.GET.get('search', '').strip()
    current_year = datetime.now().year

    # Step 1: Get the latest entry for each student based on their Name
    latest_students = (
        List.objects.filter(Course=teacher_course, Status='Approved', Year=current_year)
        .values('Name')  # Group by Name
        .annotate(latest_id=Max('id'))  # Get the latest entry for each student
    )

    # Step 2: Fetch only the latest entries (removes duplicates)
    students_query = List.objects.filter(id__in=[entry['latest_id'] for entry in latest_students])

    if search_query:
        students_query = students_query.filter(Name__icontains=search_query)

    return render(request, 'teacherPanel/listOfStudent.html', {
        'students': students_query,
        'search_query': search_query,
        'teacher_course': teacher_course
    })

def fetch_students(request):
    teacher_course = request.session.get('teacher_course', None)

    if not teacher_course:
        return JsonResponse({'error': 'No course assigned to this teacher.'}, status=400)

    search_query = request.GET.get('search', '').strip()
    current_year = datetime.now().year

    if search_query:
        students = List.objects.filter(Course=teacher_course, Status='Approved', Year=current_year, Name__icontains=search_query)
    else:
        students = List.objects.filter(Course=teacher_course, Status='Approved', Year=current_year)

    return JsonResponse({'students': list(students.values())})

def approved_studentsDeclined(request):
    if not request.session.get('teacher_id'):
        return redirect('loginForm')

    if not request.session.get('teacher_role') == 'Teacher':
        return redirect('login')

    teacher_email = request.session.get('teacher_email', None)

    if not teacher_email:
        return render(request, 'teacherPanel/teacherCourses.html', {
            'error': 'No teacher logged in.',
        })

    try:
        teacher = Admin.objects.get(Email=teacher_email)
        teacher_course = teacher.Course
    except Admin.DoesNotExist:
        return render(request, 'teacherPanel/teacherCourses.html', {
            'error': 'Teacher not found.',
        })

    search_query = request.GET.get('search', '').strip()
    current_year = datetime.now().year

    students_query = List.objects.filter(Course=teacher_course, Status='Declined', Year=current_year)

    if search_query:
        students_query = students_query.filter(Name__icontains=search_query)

    return render(request, 'teacherPanel/listOfStudentDecline.html', {
        'students': students_query,
        'search_query': search_query,
        'teacher_course': teacher_course
    })

# Add this function to handle the undo button click
def undo_student(request, student_id):
    if not request.session.get('teacher_id'):
        return redirect('loginForm')

    if not request.session.get('teacher_role') == 'Teacher':
        return redirect('login')

    try:
        student = List.objects.get(id=student_id)
        student.Status = 'Pending'  # Update status to 'Pending'
        student.save()
        return redirect('approved_students')  # Redirect back to the list of declined students
    except List.DoesNotExist:
        return render(request, 'loginForm.html', {'error': 'Student not found'})
    
def undo_studentDecline(request, student_id):
    if not request.session.get('teacher_id'):
        return redirect('loginForm')

    if not request.session.get('teacher_role') == 'Teacher':
        return redirect('login')

    try:
        student = List.objects.get(id=student_id)
        student.Status = 'Pending'  # Update status to 'Pending'
        student.save()
        return redirect('approved_studentsDeclined')  # Redirect back to the list of declined students
    except List.DoesNotExist:
        return render(request, 'loginForm.html', {'error': 'Student not found'})
   
   
def fetch_studentsDeclined(request):
    teacher_course = request.session.get('teacher_course', None)

    if not teacher_course:
        return JsonResponse({'error': 'No course assigned to this teacher.'}, status=400)

    search_query = request.GET.get('search', '').strip()
    current_year = datetime.now().year

    if search_query:
        students = List.objects.filter(Course=teacher_course, Status='Declined', Year=current_year, Name__icontains=search_query)
    else:
        students = List.objects.filter(Course=teacher_course, Status='Declined', Year=current_year)

    return JsonResponse({'students': list(students.values())})

from django.contrib import messages

from django.db import IntegrityError

def adminPanel(request):
    if not request.session.get('user_id'):
        return redirect('loginForm')

    if not request.session.get('user_role') == 'Admin':
        return redirect('loginForm')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact_no = request.POST.get('contactNo')
        rank = request.POST.get('rank')
        designation = request.POST.get('designation')
        college = request.POST.get('college')
        course = request.POST.get('course')

        if Admin.objects.filter(Email=email).exists():
            messages.error(request, 'The email account has already been used.')
            return redirect('adminPanel')

        if Admin.objects.filter(Course=course).exists():
            messages.error(request, 'The course has already been assigned to another teacher.')
            return redirect('adminPanel')

        raw_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        hashed_password = make_password(raw_password)
        full_name = f"{first_name} {middle_name} {last_name}".strip()

        try:
            send_mail(
                'Your Account Creation',
                f'Hello {full_name},\n\nYour account has been created.\n\nEmail: {email}\nPassword: {raw_password}\n\nPlease change your password after logging in.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f'Failed to send email due to the following error: {e}')
            return redirect('adminPanel')

        try:
            new_teacher = Admin(
                Name=full_name,
                Email=email,
                Rank=rank,
                Designation=designation,
                Course=course,
                Password=hashed_password,
                Address=address,
                Number=contact_no,
                College=college,
                Role='Teacher'
            )
            new_teacher.save()
            messages.success(request, 'Teacher account created and email sent successfully.')
        except IntegrityError:
            messages.error(request, 'Failed to save teacher due to a database error.')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
        return redirect('adminPanel')

    colleges = Course.objects.values('College').distinct()
    courses = Course.objects.all()

    teachers = Admin.objects.filter(Role='Teacher')
    return render(request, 'adminPanel/adminPanel.html', {
        'teachers': teachers,
        'colleges': colleges,
        'courses': courses
    })

def get_courses_by_college(request):
    if request.method == 'GET':
        college = request.GET.get('college')
        if college:
            courses = Course.objects.filter(College=college).values('id', 'Course')
            return JsonResponse({'courses': list(courses)}, safe=False)
        return JsonResponse({'error': 'No college selected.'}, status=400)

from django.db.models import Q

def delete_teacher(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            teacher_id = data.get('id')

            teacher = Admin.objects.get(id=teacher_id)

            print(f"Teacher's Course: {teacher.Course}")

            students_count = List.objects.filter(Course=teacher.Course).count()

            print(f"Number of students in course {teacher.Course}: {students_count}")

            if students_count > 0:
                return JsonResponse({
                    'success': False,
                    'message': f'Teacher cannot be deleted as there are still {students_count} students added to the list in their {teacher.Course} course.'
                })

            teacher.delete()

            return JsonResponse({'success': True, 'message': 'Teacher deleted successfully'})

        except Admin.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Teacher not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def delete_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')

        try:
            student = List.objects.get(id=student_id)
            student.delete()
            return JsonResponse({'success': True, 'message': 'Student deleted successfully'})
        except List.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Student not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def setting(request):
    if not request.session.get('teacher_id'):
        return redirect('loginForm')

    if not request.session.get('teacher_role') == 'Teacher':
        return redirect('login')

    teacher_course = request.session.get('teacher_course')
    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        messages.error(request, 'No teacher ID found in session.')
        return redirect('loginForm')

    teacher = get_object_or_404(Admin, id=teacher_id)

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        if old_password and new_password:
            if teacher.Password.startswith('pbkdf2_'):
                password_is_correct = check_password(old_password, teacher.Password)
            else:
                password_is_correct = old_password == teacher.Password

            if password_is_correct:
                teacher.Password = make_password(new_password)
                teacher.save()
                messages.success(request, 'Password changed successfully.')
            else:
                messages.error(request, 'Old password is incorrect.')
            return redirect('setting')

        teacher.Name = request.POST.get('Name', teacher.Name)
        teacher.Rank = request.POST.get('Rank', teacher.Rank)
        teacher.Designation = request.POST.get('Designation', teacher.Designation)
        teacher.Email = request.POST.get('Email', teacher.Email)
        teacher.Number = request.POST.get('Number', teacher.Number)
        teacher.Address = request.POST.get('Address', teacher.Address)
        teacher.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('setting')

    return render(request, 'teacherPanel/setting.html', {'teacher': teacher, 'teacher_course': teacher_course})

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not Admin.objects.filter(Email=email).exists():
            return JsonResponse({"success": False, "message": "Email not found."})

        otp = str(random.randint(100000, 999999))
        OTP.objects.create(email=email, otp=otp)

        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {otp}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return JsonResponse({"success": True, "message": "OTP sent to your email."})

@csrf_exempt
def reset_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        otp_code = data.get('otp')
        new_password = data.get('new_password')

        try:
            admin = Admin.objects.get(Email=email)
        except Admin.DoesNotExist:
            return JsonResponse({"success": False, "message": "Email not found."})

        otp_entry = OTP.objects.filter(email=email, otp=otp_code, is_verified=False).first()

        if not otp_entry:
            return JsonResponse({"success": False, "message": "Invalid OTP."})

        admin.Password = make_password(new_password)
        admin.save()

        otp_entry.is_verified = True
        otp_entry.save()

        return JsonResponse({"success": True, "message": "Password has been updated."})

def dashboardAdmin(request):
    if not request.session.get('user_id'):
        return redirect('loginForm')

    if not request.session.get('user_role') == 'Admin':
        return redirect('loginForm')

    teacher_count = Admin.objects.filter(Role='Teacher').count()
    student_count = Student.objects.count()
    course_count = Course.objects.count()
    feedback_count = Feedback.objects.count()

    student_usage_data = (
        Student.objects.values('Year')
        .annotate(count=Count('id'))
        .order_by('Year')
    )

    graph_data = {
        'years': [entry['Year'] for entry in student_usage_data],
        'counts': [entry['count'] for entry in student_usage_data],
    }

    course_status_data = (
        List.objects.values('Course', 'Status')
        .annotate(count=Count('id'))
        .order_by('Course', 'Status')
    )

    table_data = {}
    for entry in course_status_data:
        course_name = entry['Course']
        status = entry['Status']
        count = entry['count']

        course_obj = Course.objects.filter(Course=course_name).first()
        logo = course_obj.MainLogo if course_obj and course_obj.Logo else 'img/default_logo.png'

        if course_name not in table_data:
            table_data[course_name] = {
                'Approved': 0,
                'Declined': 0,
                'Logo': logo
            }

        if status == 'Approved':
            table_data[course_name]['Approved'] += count
        elif status == 'Declined':
            table_data[course_name]['Declined'] += count

    return render(request, 'adminPanel/dashboardAdmin.html', {
        'teacher_count': teacher_count,
        'student_count': student_count,
        'course_count': course_count,
        'feedback_count': feedback_count,
        'graph_data': json.dumps(graph_data, cls=DjangoJSONEncoder),
        'table_data': table_data,
    })

def dashboardTeacher(request):
    if not request.session.get('teacher_id'):
        return redirect('loginForm')

    if not request.session.get('teacher_role') == 'Teacher':
        return redirect('login')

    teacher_course = request.session.get('teacher_course')
    if not teacher_course:
        return render(request, 'teacherPanel/dashboardTeacher.html', {
            'status_summary': {'Approved': 0, 'Declined': 0, 'Pending': 0},
            'graph_data': json.dumps({}, cls=DjangoJSONEncoder),
            'total_students': 0,
            'error_message': 'No course found for the teacher.'
        })

    student_list = List.objects.filter(Course=teacher_course)

    total_students = student_list.count()

    status_counts = (
        student_list.values('Status')
        .annotate(count=Count('id'))
    )

    status_summary = {'Approved': 0, 'Declined': 0, 'Pending': 0}
    for entry in status_counts:
        status_summary[entry['Status']] = entry['count']

    graph_data = (
        student_list.values('Year')
        .annotate(total_students=Count('id'))
        .order_by('Year')
    )

    graph_formatted = {
        'years': [entry['Year'] for entry in graph_data],
        'total_students': [entry['total_students'] for entry in graph_data],
    }

    pending_students = student_list.filter(Status="Pending")

    return render(request, 'teacherPanel/dashboardTeacher.html', {
        'status_summary': status_summary,
        'graph_data': json.dumps(graph_formatted, cls=DjangoJSONEncoder),
        'teacher_course': teacher_course,
        'total_students': total_students,
        'pending_students': pending_students,
    })
