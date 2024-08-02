from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CustomUserCreationForm, QuestionForm, AnswerFormSet, TestForm, DragDropItemFormSet, DragDropZoneFormSet, FillInTheBlankFormSet
from .models import Test, Question, Result, User, DragDropItem, DragDropZone, FillInTheBlank
from .simulation import CommandInterpreterWrapper
import stripe
import json
from datetime import datetime
import logging
from django.utils import timezone
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from django.template.loader import render_to_string
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import smtplib
import base64

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_gmail_service():
    creds = Credentials.from_authorized_user_info(
        {
            "client_id": settings.GMAIL_OAUTH_CLIENT_ID,
            "client_secret": settings.GMAIL_OAUTH_CLIENT_SECRET,
            "refresh_token": settings.GMAIL_OAUTH_REFRESH_TOKEN,
        },
        ["https://mail.google.com/"]
    )

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds

def send_gmail(sender, to, subject, body):
    creds = get_gmail_service()
    try:
        message = MIMEText(body)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.ehlo()
        server.docmd('AUTH', 'XOAUTH2 ' + creds.token)
        server.sendmail(sender, to, message.as_string())
        server.quit()

        logger.info(f"Email sent successfully to {to}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

def home_view(request):
    return render(request, 'core/home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_welcome_email(user)
            return redirect('payment')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def send_welcome_email(user):
    subject = "Welcome to Certifly"
    message = f"Hello {user.username},\n\nWelcome to Certifly! We're excited to have you on board."
    send_gmail(settings.DEFAULT_FROM_EMAIL, user.email, subject, message)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'core/password_reset.html'
    email_template_name = 'core/password_reset_email.html'
    subject_template_name = 'core/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'core/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'core/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'core/password_reset_complete.html'

class TestView(View):
    def get(self, request, test_id=None):
        if test_id:
            test = get_object_or_404(Test, id=test_id)
            questions = test.questions.all()
            return render(request, 'core/test_taking.html', {'test': test, 'questions': questions})
        else:
            tests = Test.objects.all()
            return render(request, 'core/test_list.html', {'tests': tests})
    
    def post(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        data = json.loads(request.body)
        answers = data.get('answers')
        
        score = self.calculate_score(test, answers)
        
        Result.objects.create(
            user=request.user,
            test=test,
            score=score,
            start_time=timezone.now(),
            end_time=timezone.now(),
            answers=json.dumps(answers)
        )
        
        return JsonResponse({'success': True, 'redirect_url': reverse('dashboard')})

    def calculate_score(self, test, answers):
        total_questions = test.questions.count()
        correct_answers = 0

        for question in test.questions.all():
            question_id = str(question.id)
            if question_id in answers:
                user_answer = answers[question_id]
                if question.question_type == 'MC':
                    correct_answer = [answer.text for answer in question.answers.filter(is_correct=True)]
                    if set(user_answer) == set(correct_answer):
                        correct_answers += 1
                elif question.question_type == 'DD':
                    correct_placements = self.check_drag_drop_answer(question, user_answer)
                    if correct_placements == question.drag_drop_zones.count():
                        correct_answers += 1
                elif question.question_type == 'MAT':
                    correct_answer = [(item.left_side, item.right_side) for item in question.matching_items.all()]
                    if set(map(tuple, user_answer)) == set(map(tuple, correct_answer)):
                        correct_answers += 1
                elif question.question_type == 'FIB':
                    fill_in_the_blanks = question.fill_in_the_blanks.all()
                    if len(user_answer) == len(fill_in_the_blanks):
                        all_correct = True
                        for i, fib in enumerate(fill_in_the_blanks):
                            if user_answer[i].lower().strip() != fib.correct_answer.lower().strip():
                                all_correct = False
                                break
                        if all_correct:
                            correct_answers += 1
                elif question.question_type == 'SIM':
                    interpreter = CommandInterpreterWrapper()
                    if isinstance(user_answer, list):
                        for command in user_answer:
                            if isinstance(command, str) and command.startswith('$'):
                                interpreter.execute_command(command[1:].strip())
                    elif isinstance(user_answer, str):
                        for command in user_answer.split('\n'):
                            if command.startswith('$'):
                                interpreter.execute_command(command[1:].strip())
                    
                    simulation = question.simulations.first()
                    if simulation:
                        goal_state = simulation.expected_commands
                        if interpreter.check_goal_state(goal_state):
                            correct_answers += 1
                    else:
                        print(f"Warning: No simulation found for question {question_id}")

        return (correct_answers / total_questions) * 100

    def check_drag_drop_answer(self, question, user_answer):
        correct_placements = 0
        for zone_id, item_id in user_answer.items():
            zone = DragDropZone.objects.get(id=zone_id)
            item = DragDropItem.objects.get(id=item_id)
            if zone.correct_item == item:
                correct_placements += 1
        return correct_placements

@login_required
def create_test_view(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save()
            return redirect('create_question', test_id=test.id)
    else:
        form = TestForm()
    return render(request, 'core/create_test.html', {'form': form})

@login_required
def create_question_view(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.test = test
            
            if 'image' in request.FILES:
                result = upload(request.FILES['image'])
                question.image = result['secure_url']
            
            question.save()
            
            if question.question_type == 'MC':
                answer_formset = AnswerFormSet(request.POST, instance=question)
                if answer_formset.is_valid():
                    answer_formset.save()
            elif question.question_type == 'DD':
                item_formset = DragDropItemFormSet(request.POST, request.FILES, instance=question)
                zone_formset = DragDropZoneFormSet(request.POST, instance=question)
                if item_formset.is_valid() and zone_formset.is_valid():
                    items = item_formset.save(commit=False)
                    for item in items:
                        if item.image:
                            result = upload(item.image)
                            item.image = result['secure_url']
                        item.save()
                    zone_formset.save()
            elif question.question_type == 'FIB':
                fib_formset = FillInTheBlankFormSet(request.POST, instance=question)
                if fib_formset.is_valid():
                    fib_formset.save()
            
            return JsonResponse({'success': True, 'question_id': question.id})
    else:
        question_form = QuestionForm()
        answer_formset = AnswerFormSet()
        item_formset = DragDropItemFormSet()
        zone_formset = DragDropZoneFormSet()
        fib_formset = FillInTheBlankFormSet()
    
    return render(request, 'core/create_question.html', {
        'question_form': question_form,
        'answer_formset': answer_formset,
        'item_formset': item_formset,
        'zone_formset': zone_formset,
        'fib_formset': fib_formset,
        'test': test
    })

@staff_member_required
@csrf_exempt
def upload_question_image(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        if 'image' in request.FILES:
            result = upload(request.FILES['image'])
            question.image = result['secure_url']
            question.save()
            return JsonResponse({'success': True, 'image_url': question.image})
        else:
            return JsonResponse({'success': False, 'error': 'No image file provided'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.payment_status:
                    return redirect('dashboard')
                else:
                    return redirect('payment')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def payment_view(request):
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': settings.STRIPE_PRICE_ID,
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success')),
            cancel_url=request.build_absolute_uri(reverse('home')),
        )
        return redirect(checkout_session.url)
    return render(request, 'core/payment.html')

@login_required
def payment_success_view(request):
    user = request.user
    user.payment_status = True
    user.save()
    send_payment_confirmation_email(user)
    return redirect('dashboard')

def send_payment_confirmation_email(user):
    subject = "Payment Confirmation"
    message = f"Hello {user.username},\n\nThank you for your payment. Your account is now fully activated."
    send_gmail(settings.DEFAULT_FROM_EMAIL, user.email, subject, message)

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    if not request.user.payment_status:
        return redirect('payment')
    tests = Test.objects.all()
    latest_result = Result.objects.filter(user=request.user).order_by('-end_time').first()
    return render(request, 'core/dashboard.html', {'tests': tests, 'latest_result': latest_result})

@csrf_exempt
def execute_command(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            command = data.get('command')
            
            interpreter_state = request.session.get('command_interpreter_state')
            if interpreter_state is None:
                interpreter = CommandInterpreterWrapper(default_directory="C:\\Users\\Public")
            else:
                interpreter = CommandInterpreterWrapper.from_json(interpreter_state)
            
            result = interpreter.execute_command(command)
            
            request.session['command_interpreter_state'] = interpreter.to_json()
            
            return JsonResponse(result)
        except Exception as e:
            logger.error(f"Error in execute_command view: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def start_new_session(request):
    wrapper = CommandInterpreterWrapper(default_directory="C:\\Users\\Public")
    request.session['command_interpreter_state'] = wrapper.to_json()
    return JsonResponse({"message": "New session started"})

def handle_command(request):
    if 'command_interpreter_state' not in request.session:
        return JsonResponse({"error": "No active session"}, status=400)
    
    json_data = request.session['command_interpreter_state']
    wrapper = CommandInterpreterWrapper.from_json(json_data)
    
    command = request.POST.get('command')
    result = wrapper.execute_command(command)
    
    request.session['command_interpreter_state'] = wrapper.to_json()
    return JsonResponse(result)