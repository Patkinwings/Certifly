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
from .forms import CustomUserCreationForm, QuestionForm, AnswerFormSet, TestForm, DragDropItemFormSet, DragDropZoneFormSet, FillInTheBlankFormSet, CategoryForm
from .models import Test, Question, Result, User, DragDropItem, DragDropZone, FillInTheBlank, Category
from .simulation import CommandInterpreterWrapper
import stripe
import json
from datetime import datetime
import logging
from django.utils import timezone
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.template import loader
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str

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
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

class CustomPasswordResetView(PasswordResetView):
    template_name = 'core/password_reset.html'
    email_template_name = 'core/password_reset_email.html'
    subject_template_name = 'core/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    from_email = settings.DEFAULT_FROM_EMAIL

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain'] = get_current_site(self.request).domain
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        return context

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'core/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'core/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['validlink'] = self.validlink
        return context

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'core/password_reset_complete.html'

@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all().order_by('order')
    print(f"Test data: id={test.id}, questions_count={questions.count()}, time_limit={test.time_limit}")
    return render(request, 'core/test_taking.html', {
        'test': test,
        'questions': questions,
    })

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
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    if not request.user.payment_status:
        return redirect('payment')
    tests = Test.objects.all()
    latest_result = Result.objects.filter(user=request.user).order_by('-end_time').first()
    
    category_performance = {}
    if latest_result:
        category_scores = json.loads(latest_result.category_scores)
        for category_id, scores in category_scores.items():
            category_performance[scores['name']] = scores['percentage']
    
    return render(request, 'core/dashboard.html', {
        'tests': tests,
        'latest_result': latest_result,
        'category_performance': category_performance
    })

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

def get_password_reset_token(user):
    """
    Generate a one-use only token for resetting password.
    """
    from django.contrib.auth.tokens import default_token_generator
    return default_token_generator.make_token(user)

def send_password_reset_email(request, user):
    """
    Send a password reset email to the user.
    """
    token = get_password_reset_token(user)
    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"{protocol}://{current_site.domain}/reset/{uid}/{token}/"
    
    subject = "Password Reset for Certifly"
    message = render_to_string('core/password_reset_email.html', {
        'user': user,
        'reset_url': reset_url,
        'domain': current_site.domain,
        'site_name': 'Certifly',
        'protocol': protocol,
        'uid': uid,
        'token': token,
    })
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def custom_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            send_password_reset_email(request, user)
            return redirect('password_reset_done')
        except User.DoesNotExist:
            # We don't want to reveal whether a user exists or not,
            # so we'll still show the success page
            return redirect('password_reset_done')
    return render(request, 'core/password_reset.html')

def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                return redirect('password_reset_complete')
            else:
                return render(request, 'core/password_reset_confirm.html', {'validlink': True, 'error': 'Passwords do not match'})
    else:
        validlink = False

    return render(request, 'core/password_reset_confirm.html', {'validlink': validlink})

def custom_password_reset_complete(request):
    return render(request, 'core/password_reset_complete.html')

@login_required
def view_result_details(request, result_id):
    result = get_object_or_404(Result, id=result_id, user=request.user)
    test = result.test
    questions = test.questions.all().prefetch_related('category')
    user_answers = json.loads(result.answers)
    category_scores = json.loads(result.category_scores)

    question_details = []
    for question in questions:
        user_answer = user_answers.get(str(question.id))
        is_correct = False
        correct_answer = None

        if question.question_type == 'MC':
            correct_answer = [answer.text for answer in question.answers.filter(is_correct=True)]
            is_correct = set(user_answer) == set(correct_answer) if user_answer else False
        elif question.question_type == 'DD':
            correct_placements = 0
            for zone_id, item_id in user_answer.items():
                zone = DragDropZone.objects.get(id=zone_id)
                item = DragDropItem.objects.get(id=item_id)
                if zone.correct_item == item:
                    correct_placements += 1
            is_correct = correct_placements == question.drag_drop_zones.count()
            correct_answer = {zone.id: zone.correct_item.id for zone in question.drag_drop_zones.all()}
        elif question.question_type == 'MAT':
            correct_answer = [(item.left_side, item.right_side) for item in question.matching_items.all()]
            is_correct = set(map(tuple, user_answer)) == set(map(tuple, correct_answer)) if user_answer else False
        elif question.question_type == 'FIB':
            fill_in_the_blanks = question.fill_in_the_blanks.all()
            correct_answer = [fib.correct_answer for fib in fill_in_the_blanks]
            is_correct = all(user_answer[i].lower().strip() == correct_answer[i].lower().strip() for i in range(len(correct_answer))) if user_answer else False
        elif question.question_type == 'SIM':
            simulation = question.simulations.first()
            if simulation:
                correct_answer = simulation.expected_commands
                interpreter = CommandInterpreterWrapper()
                for command in user_answer:
                    if isinstance(command, str) and command.startswith('$'):
                        interpreter.execute_command(command[1:].strip())
                is_correct = interpreter.check_goal_state(correct_answer)
            else:
                correct_answer = "N/A"
                is_correct = False

        question_details.append({
            'question': question,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })

    return render(request, 'core/result_details.html', {
        'result': result,
        'test': test,
        'question_details': question_details,
        'category_scores': category_scores
    })

@login_required
def get_question(request, test_id, question_index):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all().order_by('order')

    if question_index < 0 or question_index >= questions.count():
        return JsonResponse({'error': 'Invalid question index'}, status=400)

    question = questions[question_index]

    question_data = {
        'id': question.id,
        'text': question.text,
        'question_type': question.question_type,
        'image': question.image.url if question.image else None,
        'options': [],
    }

    if question.question_type == 'MC':
        question_data['options'] = [{'id': answer.id, 'text': answer.text} for answer in question.answers.all()]
    elif question.question_type == 'DD':
        question_data['drag_drop_items'] = [{'id': item.id, 'text': item.text, 'image': item.image.url if item.image else None} for item in question.drag_drop_items.all()]
        question_data['drag_drop_zones'] = [{'id': zone.id, 'text': zone.text} for zone in question.drag_drop_zones.all()]
    elif question.question_type == 'MAT':
        question_data['matching_items'] = [{'id': item.id, 'left_side': item.left_side, 'right_side': item.right_side} for item in question.matching_items.all()]
    elif question.question_type == 'FIB':
        question_data['fill_in_the_blanks'] = [{'id': fib.id, 'text': fib.text} for fib in question.fill_in_the_blanks.all()]
    elif question.question_type == 'SIM':
        simulation = question.simulations.first()
        if simulation:
            question_data['simulation'] = {
                'id': simulation.id,
                'initial_state': simulation.initial_state,
            }
            if hasattr(simulation, 'goal_state'):
                question_data['simulation']['goal_state'] = simulation.goal_state
            else:
                question_data['simulation']['goal_state'] = None
                print(f"Warning: Simulation {simulation.id} does not have a goal_state attribute")

    return JsonResponse(question_data)

@login_required
def submit_answer(request, test_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        question_id = data.get('question_id')
        answer = data.get('answer')

        # Store the answer in the session
        if 'test_answers' not in request.session:
            request.session['test_answers'] = {}
        request.session['test_answers'][question_id] = answer
        request.session.modified = True

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def finish_test(request, test_id):
    if request.method == 'POST':
        test = get_object_or_404(Test, id=test_id)
        answers = request.session.get('test_answers', {})

        score, category_scores = calculate_score(test, answers)

        Result.objects.create(
            user=request.user,
            test=test,
            score=score,
            start_time=timezone.now(),
            end_time=timezone.now(),
            answers=json.dumps(answers),
            category_scores=json.dumps(category_scores)
        )

        # Clear the test answers from the session
        if 'test_answers' in request.session:
            del request.session['test_answers']

        return JsonResponse({'success': True, 'redirect_url': reverse('dashboard')})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def calculate_score(test, answers):
    total_questions = test.questions.count()
    correct_answers = 0
    category_scores = {}

    for question in test.questions.all():
        question_id = str(question.id)
        category = question.category
        if category not in category_scores:
            category_scores[category.id] = {'correct': 0, 'total': 0, 'name': str(category)}

        category_scores[category.id]['total'] += 1

        if question_id in answers:
            user_answer = answers[question_id]
            if question.question_type == 'MC':
                correct_answer = [answer.text for answer in question.answers.filter(is_correct=True)]
                if set(user_answer) == set(correct_answer):
                    correct_answers += 1
                    category_scores[category.id]['correct'] += 1
            elif question.question_type == 'DD':
                correct_placements = check_drag_drop_answer(question, user_answer)
                if correct_placements == question.drag_drop_zones.count():
                    correct_answers += 1
                    category_scores[category.id]['correct'] += 1
            elif question.question_type == 'MAT':
                correct_answer = [(item.left_side, item.right_side) for item in question.matching_items.all()]
                if set(map(tuple, user_answer)) == set(map(tuple, correct_answer)):
                    correct_answers += 1
                    category_scores[category.id]['correct'] += 1
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
                        category_scores[category.id]['correct'] += 1
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
                        category_scores[category.id]['correct'] += 1
                else:
                    print(f"Warning: No simulation found for question {question_id}")

    for category_id in category_scores:
        category_scores[category_id]['percentage'] = (category_scores[category_id]['correct'] / category_scores[category_id]['total']) * 100

    return (correct_answers / total_questions) * 100, category_scores

def check_drag_drop_answer(question, user_answer):
    correct_placements = 0
    for zone_id, item_id in user_answer.items():
        zone = DragDropZone.objects.get(id=zone_id)
        item = DragDropItem.objects.get(id=item_id)
        if zone.correct_item == item:
            correct_placements += 1
    return correct_placements

   