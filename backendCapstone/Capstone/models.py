from django.db import models
from django.utils import timezone

class Admin(models.Model):
    Email = models.EmailField(max_length=255, unique=True)  # Added max_length
    Password = models.CharField(max_length=100)
    Name = models.CharField(max_length=255, default='null')
    Rank = models.CharField(max_length=255, default='null')
    Designation = models.CharField(max_length=255, default='null')
    Course = models.CharField(max_length=255, default='null', unique=True)
    Role = models.CharField(max_length=255, default='null')
    Address = models.CharField(max_length=255, default='null')
    College = models.CharField(max_length=255, default='null')
    Number = models.CharField(max_length=20, default='null')  # Limited to 20 for phone numbers

    def __str__(self):
        return self.Email

class Course(models.Model):
    College = models.CharField(max_length=255)
    Course = models.CharField(max_length=255)
    AvgGrade = models.FloatField()  
    AvgCet = models.FloatField() 
    TotalScore = models.FloatField()
    CourseDescription = models.CharField(max_length=500)  # Increased length for descriptions
    Logo = models.CharField(max_length=500, default='img/png-clipart-computer-icons-error-information-error-angle-triangle-thumbnail-removebg-preview copy.png')
    reason = models.CharField(max_length=500, null=True)  # Increased length
    Category = models.FloatField(default=0)
    MainLogo = models.CharField(max_length=500, default='img/png-clipart-computer-icons-error-information-error-angle-triangle-thumbnail-removebg-preview copy.png')
    
    def __str__(self):
        return f"{self.Course} at {self.College}"
    
class List(models.Model):
    Name = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)  # Added max_length
    AvgGrade = models.FloatField()
    AvgCet = models.FloatField()
    Number = models.CharField(max_length=20)  # Limited for phone numbers
    ApplicationNo = models.CharField(max_length=50, default=0)  # Adjusted length
    Address = models.TextField()
    Course = models.CharField(max_length=255)
    Status = models.CharField(max_length=50, default='Pending')  # Adjusted length
    Year = models.IntegerField(default=0)
    EnglishProficiency = models.IntegerField(default=0)
    ReadingComprehension = models.IntegerField(default=0)
    ScienceProcessSkills = models.IntegerField(default=0)
    MathematicalSkills = models.IntegerField(default=0)
    AbstractLogicThinkingSkills = models.IntegerField(default=0)
    CetPicture = models.ImageField(upload_to='cet_results/', default="null", blank=True, null=True)
    GradePicture = models.ImageField(upload_to='grades/', default="null", blank=True, null=True)

    def __str__(self):
        return self.Name
    
class Feedback(models.Model):
    Name = models.CharField(max_length=255)
    Feedback = models.CharField(max_length=1000)  # Increased length for feedback

class Grades(models.Model):
    StudentID = models.FloatField(default=0)
    AvgGrade = models.FloatField(default=0)
    AvgCet = models.FloatField(default=0)
    TotalScore = models.FloatField(default=0)
    PersonalityScore = models.FloatField(default=0)
    courseName = models.CharField(max_length=255, default='General')
    Question = models.TextField(default="null")
    Category = models.FloatField(default=0)

class Student(models.Model):
    StudentID = models.FloatField()
    Year = models.IntegerField(default=0)
    
class Question(models.Model):
    text = models.CharField(max_length=500)  # Adjusted length to avoid index issues
    courseName = models.CharField(max_length=255, default='General')
    Percentage = models.FloatField(default=0)
    Category = models.FloatField(default=0)

class StudentResponse(models.Model):
    AvgGrade = models.FloatField(default=0)
    AvgCet = models.FloatField(default=0)
    StudentID = models.FloatField()
    question = models.CharField(max_length=500)  # Increased for long questions
    response = models.FloatField()
    courseName = models.CharField(max_length=255, null=True, blank=True)

class OTP(models.Model):
    email = models.EmailField(max_length=255)  # Added max_length
    otp = models.CharField(max_length=10)  # Usually OTPs are 4-10 digits
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=2)
    
class TotalPercentage(models.Model):
    CetAvgPercentage = models.FloatField(default=0)
    GradeAvgPercentage = models.FloatField(default=0)
    PersonalityPercentage = models.FloatField(default=0) 
