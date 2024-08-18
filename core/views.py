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
from .models import Test, Question, Result, User, DragDropItem, DragDropZone, FillInTheBlank, Category, Simulation, QuestionResult
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
from django.db import transaction

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

def home_view(request):
    return render(request, 'core/home.html')

def get_initial_state(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        initial_state = {'prompt': 'C:\\> '}
        return JsonResponse(initial_state)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

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
            elif question.question_type == 'SIM':
                expected_commands = request.POST.get('expected_commands')
                Simulation.objects.create(question=question, expected_commands=expected_commands)
            
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
        category_scores = latest_result.category_scores
        if isinstance(category_scores, str):
            try:
                category_scores = json.loads(category_scores)
            except json.JSONDecodeError:
                category_scores = {}
        for category_id, scores in category_scores.items():
            category_performance[scores['name']] = scores['percentage']
    
    return render(request, 'core/dashboard.html', {
        'tests': tests,
        'latest_result': latest_result,
        'category_performance': category_performance
    })

def execute_command(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            command = data.get('command')
            logger.debug(f"Received command: {command}")
            
            interpreter_state = request.session.get('command_interpreter_state')
            logger.debug(f"Interpreter state from session: {interpreter_state}")
            
            if interpreter_state is None:
                logger.info("Creating new CommandInterpreterWrapper")
                interpreter = CommandInterpreterWrapper(default_directory="C:\\")
            else:
                logger.info("Restoring CommandInterpreterWrapper from state")
                interpreter = CommandInterpreterWrapper.from_json(interpreter_state)
            
            if interpreter.get_current_directory() in ['.', '']:
                interpreter.set_default_directory("C:\\")
            
            logger.debug(f"Current directory before execution: {interpreter.get_current_directory()}")
            result = interpreter.execute_command(command)
            logger.debug(f"Command result: {result}")
            logger.debug(f"Current directory after execution: {interpreter.get_current_directory()}")
            
            command_history = request.session.get('command_history', [])
            command_history.insert(0, command)
            command_history = command_history[:50]
            request.session['command_history'] = command_history
            
            new_state = interpreter.to_json()
            logger.debug(f"New interpreter state: {new_state}")
            request.session['command_interpreter_state'] = new_state
            request.session.modified = True
            
            result['prompt'] = interpreter.get_prompt()
            result['command_history'] = command_history
            
            return JsonResponse(result)
        except Exception as e:
            logger.exception(f"Error in execute_command view: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def get_command_history(request):
    if request.method == 'GET':
        command_history = request.session.get('command_history', [])
        return JsonResponse({'command_history': command_history})
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
    from django.contrib.auth.tokens import default_token_generator
    return default_token_generator.make_token(user)

def send_password_reset_email(request, user):
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
    questions = test.questions.all().prefetch_related('category', 'answers', 'drag_drop_items', 'drag_drop_zones', 'matching_items', 'fill_in_the_blanks', 'simulations')
    question_results = result.question_results.all()

    question_details = []
    for question, question_result in zip(questions, question_results):
        user_answer = json.loads(question_result.user_answer)
        question_detail = {
            'question': question,
            'user_answer': user_answer,
            'is_correct': question_result.is_correct,
        }
        
        if question.question_type == 'DD':
            question_detail['drag_drop_items'] = list(question.drag_drop_items.all())
            question_detail['drag_drop_zones'] = list(question.drag_drop_zones.all())
            question_detail['user_placements'] = user_answer
            question_detail['correct_placements'] = {str(zone.id): str(zone.correct_item.id) for zone in question_detail['drag_drop_zones']}
        
        question_details.append(question_detail)

    category_scores = json.loads(result.category_scores) if isinstance(result.category_scores, str) else result.category_scores

    context = {
        'result': result,
        'test': test,
        'question_details': question_details,
        'category_scores': category_scores
    }

    return render(request, 'core/result_details.html', context)

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
       question_data['drag_drop_zones'] = [{'id': zone.id, 'label': zone.label} for zone in question.drag_drop_zones.all()]
   elif question.question_type == 'MAT':
       question_data['matching_items'] = [{'id': item.id, 'left_side': item.left_side, 'right_side': item.right_side} for item in question.matching_items.all()]
   elif question.question_type == 'FIB':
       question_data['fill_in_the_blanks'] = [{'id': fib.id, 'blank_index': fib.blank_index, 'correct_answer': fib.correct_answer} for fib in question.fill_in_the_blanks.all()]
   elif question.question_type == 'SIM':
       simulation = question.simulations.first()
       if simulation:
           question_data['simulation'] = {
               'id': simulation.id,
               'expected_commands': simulation.expected_commands,
           }

   return JsonResponse(question_data)

@login_required
def submit_answer(request, test_id):
   if request.method == 'POST':
       data = json.loads(request.body)
       question_id = data.get('question_id')
       answer = data.get('answer')

       if 'test_answers' not in request.session:
           request.session['test_answers'] = {}
       request.session['test_answers'][question_id] = answer
       request.session.modified = True

       return JsonResponse({'success': True})

   return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def finish_test(request, test_id):
    if request.method == 'POST':
        try:
            logger.info(f"Finishing test {test_id} for user {request.user.username}")
            logger.debug(f"Raw request body: {request.body.decode('utf-8')}")
            
            data = json.loads(request.body)
            answers = data.get('answers', {})
            logger.info(f"Received answers: {json.dumps(answers, indent=2)}")
            
            test = get_object_or_404(Test, id=test_id)
            score, category_scores, question_results = calculate_score(test, answers)
            
            result = Result.objects.create(
                user=request.user,
                test=test,
                score=score,
                start_time=request.session.get('test_start_time', timezone.now()),
                end_time=timezone.now(),
                answers=json.dumps(answers),
                category_scores=json.dumps(category_scores)
            )
            
            QuestionResult.objects.bulk_create([
                QuestionResult(
                    result=result,
                    question_id=qr['question_id'],
                    user_answer=json.dumps(qr['user_answer']),
                    is_correct=qr['is_correct']
                ) for qr in question_results
            ])
            
            logger.info(f"Test {test_id} finished successfully for user {request.user.username}")
            return JsonResponse({'success': True, 'redirect_url': reverse('view_result_details', args=[result.id])})
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in finish_test: {str(e)}", exc_info=True)
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            logger.error(f"Error in finish_test: {str(e)}", exc_info=True)
            return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)
    else:
        logger.warning(f"Invalid request method ({request.method}) for finish_test")
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def calculate_score(test, answers):
    logger.info(f"Calculating score for test {test.id}")
    logger.info(f"Received answers: {json.dumps(answers, indent=2)}")
    total_questions = test.questions.count()
    correct_answers = 0
    category_scores = {}
    question_results = []

    for question in test.questions.all():
        question_id = str(question.id)
        category = question.category
        logger.info(f"Processing question {question_id}, type: {question.question_type}, category: {category}")

        if category is None:
            logger.warning(f"Question {question_id} has no category assigned")
            category_id = 'uncategorized'
            category_name = 'Uncategorized'
        else:
            category_id = str(category.id)
            category_name = str(category)

        if category_id not in category_scores:
            category_scores[category_id] = {'correct': 0, 'total': 0, 'name': category_name}

        category_scores[category_id]['total'] += 1

        is_correct = False
        user_answer = answers.get(question_id)
        
        if user_answer is not None:
            logger.info(f"User answer for question {question_id}: {json.dumps(user_answer, indent=2)}")

            if question.question_type == 'MC':
                correct_answer = [str(answer.id) for answer in question.answers.filter(is_correct=True)]
                logger.info(f"Correct answer for MC question {question_id}: {correct_answer}")
                user_answer = [str(ans) for ans in user_answer]
                is_correct = set(user_answer) == set(correct_answer)
                logger.info(f"Is correct: {is_correct}")
            elif question.question_type == 'DD':
                correct_placements = check_drag_drop_answer(question, user_answer)
                logger.info(f"Correct placements for DD question {question_id}: {correct_placements}")
                is_correct = correct_placements == question.drag_drop_zones.count()
                logger.info(f"Is correct: {is_correct}")
            elif question.question_type == 'MAT':
                correct_answer = [(item.left_side, item.right_side) for item in question.matching_items.all()]
                logger.info(f"Correct answer for MAT question {question_id}: {correct_answer}")
                is_correct = set(map(tuple, user_answer)) == set(map(tuple, correct_answer))
                logger.info(f"Is correct: {is_correct}")
            elif question.question_type == 'FIB':
                fill_in_the_blanks = question.fill_in_the_blanks.all()
                correct_answers_fib = [fib.correct_answer.lower().strip() for fib in fill_in_the_blanks]
                logger.info(f"Correct answers for FIB question {question_id}: {correct_answers_fib}")
                is_correct = all(user_answer[i].lower().strip() == correct_answer for i, correct_answer in enumerate(correct_answers_fib))
                logger.info(f"Is correct: {is_correct}")
            elif question.question_type == 'SIM':
                simulation = question.simulations.first()
                if simulation:
                    expected_commands = simulation.expected_commands.split('\n')
                    user_commands = user_answer if isinstance(user_answer, list) else json.loads(user_answer)
                    
                    user_commands = [cmd.strip().lower() for cmd in user_commands if cmd.strip()]
                    expected_commands = [cmd.strip().lower() for cmd in expected_commands if cmd.strip()]
                    
                    logger.info(f"Expected commands for SIM question {question_id}: {expected_commands}")
                    logger.info(f"User commands for SIM question {question_id}: {user_commands}")
                    
                    all_commands_present = True
                    user_command_index = 0
                    for expected_cmd in expected_commands:
                        found = False
                        while user_command_index < len(user_commands):
                            if expected_cmd in user_commands[user_command_index]:
                                found = True
                                user_command_index += 1
                                break
                            user_command_index += 1
                        if not found:
                            all_commands_present = False
                            break
                    
                    is_correct = all_commands_present
                    logger.info(f"Is correct: {is_correct}")
                else:
                    logger.warning(f"No simulation found for question {question_id}")
            else:
                logger.warning(f"Unknown question type for question {question_id}: {question.question_type}")

            if is_correct:
                correct_answers += 1
                category_scores[category_id]['correct'] += 1
        else:
            logger.warning(f"No answer provided for question {question_id}")

        question_results.append({
            'question_id': question.id,
            'user_answer': user_answer,
            'is_correct': is_correct
        })

    for category_id in category_scores:
        if category_scores[category_id]['total'] > 0:
            category_scores[category_id]['percentage'] = (category_scores[category_id]['correct'] / category_scores[category_id]['total']) * 100
        else:
            category_scores[category_id]['percentage'] = 0

    final_score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    logger.info(f"Final score: {final_score}, Correct answers: {correct_answers}, Total questions: {total_questions}")
    logger.info(f"Category scores: {json.dumps(category_scores, indent=2)}")
    logger.info(f"Returning: final_score={final_score}, category_scores={category_scores}, question_results={question_results}")
    return final_score, category_scores, question_results

def check_drag_drop_answer(question, user_answer):
   correct_placements = 0
   for zone_id, item_id in user_answer.items():
       zone = DragDropZone.objects.get(id=zone_id)
       item = DragDropItem.objects.get(id=item_id)
       if zone.correct_item == item:
           correct_placements += 1
   return correct_placements