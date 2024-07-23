from core.models import Test, Question, Answer, DragDropItem, MatchingItem, Simulation

def score_test(user_answers, test_id):
    test = Test.objects.get(id=test_id)
    questions = test.questions.all()
    score = 0
    total_questions = questions.count()

    for question in questions:
        if question.question_type in ['MC', 'MCM']:
            score += score_multiple_choice(question, user_answers.get(str(question.id), []))
        elif question.question_type == 'DD':
            score += score_drag_and_drop(question, user_answers.get(str(question.id), []))
        elif question.question_type == 'SIM':
            score += score_simulation(question, user_answers.get(str(question.id), ''))
        elif question.question_type == 'MAT':
            score += score_matching(question, user_answers.get(str(question.id), {}))
        elif question.question_type == 'FIB':
            score += score_fill_in_blank(question, user_answers.get(str(question.id), ''))

    return (score / total_questions) * 100

def score_multiple_choice(question, user_answer):
    correct_answers = question.answers.filter(is_correct=True)
    if question.question_type == 'MC':
        return 1 if user_answer and user_answer[0] in correct_answers.values_list('id', flat=True) else 0
    else:  # MCM
        correct_answer_ids = set(correct_answers.values_list('id', flat=True))
        user_answer_ids = set(user_answer)
        return len(correct_answer_ids.intersection(user_answer_ids)) / len(correct_answer_ids)

def score_drag_and_drop(question, user_answer):
    correct_positions = {item.id: item.correct_position for item in question.drag_drop_items.all()}
    correct_count = sum(1 for item_id, position in user_answer.items() if correct_positions.get(int(item_id)) == position)
    return correct_count / len(correct_positions)

def score_simulation(question, user_answer):
    simulation = question.simulations.first()
    if not simulation:
        return 0
    expected_commands = set(simulation.expected_commands.split('\n'))
    user_commands = set(user_answer.split('\n'))
    return len(expected_commands.intersection(user_commands)) / len(expected_commands)

def score_matching(question, user_answer):
    correct_matches = {item.left_side: item.right_side for item in question.matching_items.all()}
    correct_count = sum(1 for left, right in user_answer.items() if correct_matches.get(left) == right)
    return correct_count / len(correct_matches)

def score_fill_in_blank(question, user_answer):
    correct_answer = question.answers.filter(is_correct=True).first()
    if not correct_answer:
        return 0
    return 1 if user_answer.lower().strip() == correct_answer.text.lower().strip() else 0