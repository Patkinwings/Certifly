# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .forms import CustomUserCreationForm, QuestionForm, AnswerFormSet, TestForm, DragDropItemFormSet, DragDropZoneFormSet, FillInTheBlankFormSet
from .models import Test, Question, Result, User, DragDropItem, DragDropZone, FillInTheBlank
from .simulation import CommandInterpreterWrapper
from .google_auth import get_gmail_service
import stripe
import json
from datetime import datetime
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    recipient_list = [user.email]
    send_email(subject, message, recipient_list)

def send_email(subject, message, recipient_list):
    creds = get_gmail_service()
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        auth_user=settings.EMAIL_HOST_USER,
        auth_password=creds.token,
        connection=None
    )

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
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.test = test
            question.save()
            
            if question.question_type == 'MC':
                answer_formset = AnswerFormSet(request.POST, instance=question)
                if answer_formset.is_valid():
                    answer_formset.save()
            elif question.question_type == 'DD':
                item_formset = DragDropItemFormSet(request.POST, instance=question)
                zone_formset = DragDropZoneFormSet(request.POST, instance=question)
                if item_formset.is_valid() and zone_formset.is_valid():
                    item_formset.save()
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

@login_required
@csrf_exempt
def upload_question_image(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id)
        if 'image' in request.FILES:
            question.image = request.FILES['image']
            question.image_upload_status = 'completed'
            question.save()
            return JsonResponse({'success': True, 'image_url': question.image.url})
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
    recipient_list = [user.email]
    send_email(subject, message, recipient_list)

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
                interpreter = CommandInterpreterWrapper()
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