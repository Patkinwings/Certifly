console.log("test_taking.js loaded");

let answers = {};
let testDuration;
let endTime;
let currentQuestionIndex = 0;
let isLoading = false;
let totalQuestions = 0;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateTimer(endTime) {
    const timerElement = document.getElementById('test-timer');
    if (!timerElement) {
        console.error("Timer element not found");
        return;
    }

    function updateDisplay() {
        const now = new Date().getTime();
        const distance = endTime - now;

        if (distance < 0) {
            console.log("Time's up!");
            clearInterval(timerInterval);
            timerElement.innerHTML = "Time's up!";
            finishTest();
            return;
        }

        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        timerElement.innerHTML = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    updateDisplay();
    const timerInterval = setInterval(updateDisplay, 1000);
}

function initializeTimer() {
    console.log("Initializing timer");
    if (isNaN(testDuration)) {
        console.error("Invalid test duration:", testDuration);
        return;
    }
    const endTime = new Date().getTime() + testDuration * 60 * 1000;
    updateTimer(endTime);
}

function renderMultipleChoice(data) {
    console.log("Rendering multiple choice question");
    let optionsHtml = '<div class="options">';
    data.options.forEach(option => {
        optionsHtml += `
            <div>
                <input type="checkbox" id="option_${option.id}" name="question_${data.id}" value="${option.id}">
                <label for="option_${option.id}">${option.text}</label>
            </div>
        `;
    });
    optionsHtml += '</div>';
    return optionsHtml;
}

function renderDragAndDrop(data) {
    console.log("Rendering drag and drop question", data);
    let html = '<div class="drag-drop-container">';
    html += '<div class="drag-items">';
    data.drag_drop_items.forEach(item => {
        let itemContent = '';
        if (item.image) {
            itemContent = `<img src="${item.image}" alt="${item.text}" style="max-width: 100px; max-height: 100px;">`;
        } else {
            itemContent = item.text;
        }
        html += `<div class="drag-item" draggable="true" data-item-id="${item.id}">${itemContent}</div>`;
    });
    html += '</div>';
    html += '<div class="drop-zones">';
    data.drag_drop_zones.forEach(zone => {
        html += `<div class="drop-zone" data-zone-id="${zone.id}">${zone.label}</div>`;
    });
    html += '</div></div>';
    return html;
}

function renderMatching(data) {
    console.log("Rendering matching question");
    let html = '<div class="matching-container">';
    html += '<div class="left-items">';
    data.matching_items.forEach(item => {
        html += `<div class="match-item" data-item-id="${item.id}">${item.left_side}</div>`;
    });
    html += '</div>';
    html += '<div class="right-items">';
    data.matching_items.forEach(item => {
        html += `<div class="match-item" data-item-id="${item.id}">${item.right_side}</div>`;
    });
    html += '</div></div>';
    return html;
}

function renderFillInTheBlank(data) {
    console.log("Rendering fill in the blank question");
    let html = '<div class="fill-in-the-blank-container">';
    data.fill_in_the_blanks.forEach((blank, index) => {
        html += `<input type="text" name="blank_${index}" placeholder="Fill in the blank">`;
    });
    html += '</div>';
    return html;
}

function renderSimulation(data) {
    console.log("Rendering simulation question", data);
    return `
        <div class="simulation-container" data-question-id="${data.id}">
            <div class="terminal"></div>
            <div class="expected-commands" style="display: none;">${data.simulation ? data.simulation.expected_commands : ''}</div>
        </div>
    `;
}

function renderQuestionType(data) {
    console.log("Rendering question type:", data.question_type);
    const testContainer = document.getElementById('question-container');
    let questionHtml = '';
    switch(data.question_type) {
        case 'MC':
            questionHtml = renderMultipleChoice(data);
            break;
        case 'DD':
            console.log("Rendering drag and drop question");
            questionHtml = renderDragAndDrop(data);
            break;
        case 'MAT':
            questionHtml = renderMatching(data);
            break;
        case 'FIB':
            questionHtml = renderFillInTheBlank(data);
            break;
        case 'SIM':
            questionHtml = renderSimulation(data);
            break;
        default:
            console.error("Unknown question type:", data.question_type);
            return;
    }
    testContainer.innerHTML += questionHtml;
    
    if (data.question_type === 'MC') {
        initializeMultipleChoice();
    } else if (data.question_type === 'DD') {
        console.log("Initializing drag and drop");
        initializeDragAndDrop();
    } else if (data.question_type === 'MAT') {
        initializeMatching();
    } else if (data.question_type === 'FIB') {
        initializeFillInTheBlank();
    } else if (data.question_type === 'SIM') {
        initializeSimulations();
    }

    // Add submit button for each question
    const submitButton = document.createElement('button');
    submitButton.type = 'button';
    submitButton.className = 'submit-answer submit-answer-initial';
    submitButton.textContent = 'Submit Answer';
    submitButton.addEventListener('click', function() {
        storeAnswer(data.id);
        console.log(`Answer submitted for question ${data.id}`);
        this.className = 'submit-answer submit-answer-saved';
        this.textContent = 'Answer Saved';
        setTimeout(() => {
            this.className = 'submit-answer submit-answer-initial';
            this.textContent = 'Submit Answer';
        }, 2000);  // Reset after 2 seconds
    });
    testContainer.appendChild(submitButton);
}

function storeAnswer(questionId) {
    console.log("Attempting to store answer for question:", questionId);
    
    let answer = getAnswerForCurrentQuestion();
    console.log(`Answer for question ${questionId}:`, answer);

    if (answer !== null) {
        answers[questionId] = answer;
        console.log(`Stored answer for question ${questionId}:`, answer);
        
        // Update all navigation buttons
        const navButtons = document.querySelectorAll('.question-nav-button');
        navButtons.forEach((button, index) => {
            if (index === currentQuestionIndex) {
                button.classList.add('answered');
                button.style.backgroundColor = '#28a745';  // Green
                console.log(`Updated navigation button for question ${questionId}`);
            }
        });
        
        // Update submit button appearance
        const submitButton = document.querySelector('.submit-answer');
        if (submitButton) {
            submitButton.classList.remove('submit-answer-initial');
            submitButton.classList.add('submit-answer-saved');
            submitButton.textContent = 'Answer Saved';
            submitButton.style.backgroundColor = '#007bff';  // Blue
            console.log(`Submit button updated for question ${questionId}`);
            
            setTimeout(() => {
                submitButton.classList.remove('submit-answer-saved');
                submitButton.classList.add('submit-answer-initial');
                submitButton.textContent = 'Submit Answer';
                submitButton.style.backgroundColor = '#28a745';  // Green
                console.log(`Submit button reset for question ${questionId}`);
            }, 2000);
        } else {
            console.error(`Submit button not found`);
        }
    } else {
        console.warn(`No answer collected for question ${questionId}`);
    }

    console.log("Current answers:", answers);
}

function checkNavigationButtons() {
    const buttons = document.querySelectorAll('.question-nav-button');
    buttons.forEach((button, index) => {
        console.log(`Button ${index + 1}: class="${button.className}", style="${button.style.cssText}", data-question-id="${button.dataset.questionId}"`);
    });
}

function loadQuestion(index) {
    if (isLoading) {
        console.log("Already loading a question, ignoring request");
        return;
    }
    
    isLoading = true;
    console.log("Loading question at index:", index);
    const testForm = document.getElementById('test-form');
    if (!testForm) {
        console.error('Test form not found in loadQuestion');
        isLoading = false;
        return;
    }
    console.log("Test form dataset in loadQuestion:", testForm.dataset);
    
    const testId = parseInt(testForm.dataset.testId);
    
    if (isNaN(testId) || isNaN(totalQuestions)) {
        console.error('Invalid test data in loadQuestion', { testId, totalQuestions });
        isLoading = false;
        return;
    }
    
    // Store the answer for the previous question before loading the new one
    if (currentQuestionIndex !== index) {
        storeAnswer(currentQuestionIndex);
    }

    console.log("Making AJAX request to load question");
    fetch(`/test/${testId}/question/${index}/`)
        .then(response => {
            console.log("Received response from server:", response);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Parsed question data:", data);
            const testContainer = document.getElementById('question-container');
            if (!testContainer) {
                console.error('Question container not found');
                isLoading = false;
                return;
            }
            
            // Store the timer element before updating the container
            const timerElement = document.getElementById('test-timer');
            
            console.log("Updating question container HTML");
            testContainer.innerHTML = `
                <div class="question-container" data-question-id="${data.id}" data-question-type="${data.question_type}">
                    <h2>Question ${index + 1}</h2>
                    <p>${data.text}</p>
                    ${data.image ? `<img src="${data.image}" alt="Question Image">` : ''}
                </div>
            `;
            console.log("Question type:", data.question_type);
            renderQuestionType(data);

            // Update navigation buttons
            updateNavigationButtons();
            updateQuestionNavigation(index);

            // Update the navigation button's data-question-id and color
            const navButton = document.querySelector(`.question-nav-button[data-index="${index}"]`);
            if (navButton) {
                navButton.dataset.questionId = data.id.toString();
                if (answers[data.id]) {
                    navButton.classList.add('answered');
                    navButton.style.backgroundColor = '#28a745';  // Green
                } else {
                    navButton.classList.remove('answered');
                    navButton.style.backgroundColor = '#007bff';  // Blue
                }
                console.log(`Updated navigation button for question ${data.id}, answered: ${!!answers[data.id]}`);
            } else {
                console.error(`Navigation button not found for index ${index}`);
            }

            console.log("Navigation buttons updated");

            // Reinsert the timer at the top of the question container
            if (timerElement) {
                testContainer.insertBefore(timerElement, testContainer.firstChild);
                console.log("Timer element moved to top of question container");
            }

            // Restore previously stored answer
            if (answers[data.id]) {
                console.log("Restoring previous answer for question", data.id);
                restoreAnswer(data, answers[data.id]);
                
                // Update the submit button to show "Answer Saved"
                const submitButton = testContainer.querySelector('.submit-answer');
                if (submitButton) {
                    submitButton.classList.remove('submit-answer-initial');
                    submitButton.classList.add('submit-answer-saved');
                    submitButton.textContent = 'Answer Saved';
                    submitButton.style.backgroundColor = '#007bff';  // Blue
                }
            }

            currentQuestionIndex = index;
            isLoading = false;
            console.log("Question loaded successfully");
        })
        .catch(error => {
            console.error('Error in loadQuestion:', error);
            console.error('Error stack:', error.stack);
            isLoading = false;
        });
}

function updateNavigationButtons() {
    const prevButton = document.getElementById('prev-question');
    const nextButton = document.getElementById('next-question');
    const finishButton = document.getElementById('finish-test');

    if (prevButton) prevButton.style.display = currentQuestionIndex === 0 ? 'none' : 'inline';
    if (nextButton) nextButton.style.display = currentQuestionIndex === totalQuestions - 1 ? 'none' : 'inline';
    if (finishButton) finishButton.style.display = currentQuestionIndex === totalQuestions - 1 ? 'inline' : 'none';

    console.log("Navigation buttons updated", { 
        currentQuestionIndex, 
        totalQuestions, 
        prevButtonVisible: prevButton ? prevButton.style.display : 'N/A',
        nextButtonVisible: nextButton ? nextButton.style.display : 'N/A',
        finishButtonVisible: finishButton ? finishButton.style.display : 'N/A'
    });
}

function setupNavigationButtons() {
    const prevButton = document.getElementById('prev-question');
    const nextButton = document.getElementById('next-question');
    const finishButton = document.getElementById('finish-test');

    console.log("Setting up navigation buttons");
    console.log("Previous button:", prevButton);
    console.log("Next button:", nextButton);
    console.log("Finish button:", finishButton);

    if (prevButton) {
        prevButton.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("Previous question button clicked");
            if (currentQuestionIndex > 0 && !isLoading) {
                console.log("Storing answer before moving to previous question");
                storeAnswer(currentQuestionIndex);
                currentQuestionIndex--;
                console.log("Loading previous question, new index:", currentQuestionIndex);
                loadQuestion(currentQuestionIndex);
            } else {
                console.log("Cannot move to previous question", { currentQuestionIndex, isLoading });
            }
        });
    }

    if (nextButton) {
        nextButton.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("Next question button clicked");
            if (currentQuestionIndex < totalQuestions - 1 && !isLoading) {
                console.log("Storing answer before moving to next question");
                storeAnswer(currentQuestionIndex);
                currentQuestionIndex++;
                console.log("Loading next question, new index:", currentQuestionIndex);
                loadQuestion(currentQuestionIndex);
            } else {
                console.log("Cannot move to next question", { currentQuestionIndex, totalQuestions, isLoading });
            }
        });
    }

    if (finishButton) {
        finishButton.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("Finish test button clicked");
            if (!isLoading) {
                console.log("Storing final answer before finishing test");
                storeAnswer(currentQuestionIndex);
                console.log("Initiating test finish process");
                finishTest();
            } else {
                console.log("Cannot finish test, still loading", { isLoading });
            }
        });
    }

    console.log("Navigation buttons setup completed");
    updateNavigationButtons(); // Update button visibility initially
}

function initializeTestTaking() {
    console.log("Initializing test taking");
    const testForm = document.getElementById('test-form');
    if (!testForm) {
        console.error('Test form not found in initializeTestTaking');
        return;
    }
    console.log("Test form dataset in initializeTestTaking:", testForm.dataset);
    
    const testId = parseInt(testForm.dataset.testId);
    totalQuestions = parseInt(testForm.dataset.totalQuestions);
    testDuration = parseInt(testForm.dataset.duration, 10);
    
    console.log("Parsed values in initializeTestTaking:", { testId, totalQuestions, testDuration });

    if (isNaN(testId) || isNaN(totalQuestions) || isNaN(testDuration)) {
        console.error('Invalid test data in initializeTestTaking', { testId, totalQuestions, testDuration });
        return;
    }

    try {
        populateQuestionNavigation(totalQuestions);
        loadQuestion(currentQuestionIndex);
        initializeTimer();
        setupNavigationButtons();
        updateQuestionNavigation(currentQuestionIndex);
    } catch (error) {
        console.error('Error in initializeTestTaking:', error);
        console.error('Error stack:', error.stack);
    }
}

function restoreAnswer(data, answer) {
    console.log("Restoring answer for question type:", data.question_type);
    const questionContainer = document.getElementById('question-container');
    switch (data.question_type) {
        case 'MC':
            answer.forEach(optionId => {
                const checkbox = questionContainer.querySelector(`input[value="${optionId}"]`);
                if (checkbox) checkbox.checked = true;
            });
            break;
        case 'DD':
            for (const [zoneId, itemId] of Object.entries(answer)) {
                const zone = questionContainer.querySelector(`.drop-zone[data-zone-id="${zoneId}"]`);
                const item = questionContainer.querySelector(`.drag-item[data-item-id="${itemId}"]`);
                if (zone && item) zone.appendChild(item);
            }
            break;
        case 'MAT':
            answer.forEach(([leftSide, rightSide]) => {
                const leftItem = questionContainer.querySelector(`.left-items .match-item:not(.matched):contains("${leftSide}")`);
                const rightItem = questionContainer.querySelector(`.right-items .match-item:not(.matched):contains("${rightSide}")`);
                if (leftItem && rightItem) {
                    leftItem.classList.add('matched');
                    rightItem.classList.add('matched');
                }
            });
            break;
        case 'FIB':
            const inputs = questionContainer.querySelectorAll('input[type="text"]');
            answer.forEach((value, index) => {
                if (inputs[index]) inputs[index].value = value;
            });
            break;
        case 'SIM':
            const container = questionContainer.querySelector('.simulation-container');
            if (container) container.dataset.commandHistory = JSON.stringify(answer);
            break;
        default:
            console.error("Unknown question type when restoring answer:", data.question_type);
    }
    console.log("Answer restored");
}

function getAnswerForCurrentQuestion() {
    const questionContainer = document.getElementById('question-container');
    const questionType = questionContainer.querySelector('[data-question-type]')?.dataset.questionType;
    
    if (!questionType) {
        console.error("Question type not found");
        return null;
    }
    
    console.log("Getting answer for question type:", questionType);
    
    switch (questionType) {
        case 'MC':
            return Array.from(questionContainer.querySelectorAll('input[type="checkbox"]:checked, input[type="radio"]:checked')).map(input => input.value);
        case 'DD':
            const dropZones = questionContainer.querySelectorAll('.drop-zone');
            const answer = {};
            dropZones.forEach(zone => {
                const zoneId = zone.dataset.zoneId;
                const item = zone.querySelector('.drag-item');
                answer[zoneId] = item ? item.dataset.itemId : null;
            });
            return answer;
        case 'MAT':
            const matchedPairs = [];
            const leftItems = questionContainer.querySelectorAll('.left-items .match-item.matched');
            leftItems.forEach(item => {
                const rightItem = questionContainer.querySelector(`.right-items .match-item.matched[data-item-id="${item.dataset.itemId}"]`);
                if (rightItem) {
                    matchedPairs.push([item.textContent.trim(), rightItem.textContent.trim()]);
                }
            });
            return matchedPairs;
        case 'FIB':
            return Array.from(questionContainer.querySelectorAll('input[type="text"]')).map(input => input.value);
        case 'SIM':
            const container = questionContainer.querySelector('.simulation-container');
            return container ? JSON.parse(container.dataset.commandHistory || '[]') : [];
        default:
            console.warn(`Unknown question type: ${questionType}`);
            return null;
    }
}

function finishTest() {
    console.log("Finishing test");
    storeAnswer(currentQuestionIndex); // Store the answer for the current question
    
    console.log("All stored answers:", JSON.stringify(answers, null, 2));

    if (Object.keys(answers).length === 0) {
        console.warn("No answers collected. Check if answers are being properly stored.");
    }

    const testId = document.getElementById('test-form').dataset.testId;
    const dataToSend = {answers: answers};
    
    fetch(`/test/${testId}/finish/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(dataToSend)
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Test finished successfully, redirecting to:", data.redirect_url);
            window.location.href = data.redirect_url;
        } else {
            console.error('Error finishing test:', data.error);
        }
    })
    .catch(error => {
        console.error('Error finishing test:', error);
    });
}

function initializeQuestionCreation() {
    console.log("Initializing question creation");
    const questionTypeSelect = document.getElementById('id_question_type');
    const answerFormset = document.getElementById('answer-formset');
    const dragDropFormset = document.getElementById('drag-drop-formset');
    const fibFormset = document.getElementById('fill-in-the-blank-formset');

    if (questionTypeSelect) {
        function toggleFormsets() {
            console.log("Toggling formsets for question type:", questionTypeSelect.value);
            if (questionTypeSelect.value === 'MC') {
                answerFormset.style.display = 'block';
                dragDropFormset.style.display = 'none';
                fibFormset.style.display = 'none';
            } else if (questionTypeSelect.value === 'DD') {
                answerFormset.style.display = 'none';
                dragDropFormset.style.display = 'block';
                fibFormset.style.display = 'none';
            } else if (questionTypeSelect.value === 'FIB') {
                answerFormset.style.display = 'none';
                dragDropFormset.style.display = 'none';
                fibFormset.style.display = 'block';
            } else {
                answerFormset.style.display = 'none';
                dragDropFormset.style.display = 'none';
                fibFormset.style.display = 'none';
            }
        }

        questionTypeSelect.addEventListener('change', toggleFormsets);
        toggleFormsets();
    }

    const questionForm = document.getElementById('question-form');
    if (questionForm) {
        questionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log("Submitting question form");
            const formData = new FormData(questionForm);
            fetch(questionForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Question created successfully, question ID:", data.question_id);
                    document.getElementById('image-upload-form').style.display = 'block';
                    document.getElementById('image-form').dataset.questionId = data.question_id;
                } else {
                    console.error('Error creating question:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    const imageForm = document.getElementById('image-form');
    if (imageForm) {
        imageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log("Submitting image form");
            const formData = new FormData(imageForm);
            fetch(`/upload_question_image/${imageForm.dataset.questionId}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Image uploaded successfully');
                    document.getElementById('image-upload-form').style.display = 'none';
                } else {
                    console.error('Error uploading image:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
}

function initializeMultipleChoice() {
    console.log("Initializing multiple choice questions");
    const mcQuestions = document.querySelectorAll('.question[data-question-type="MC"]');
    mcQuestions.forEach(question => {
        const inputs = question.querySelectorAll('input[type="checkbox"], input[type="radio"]');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                if (this.type === 'radio') {
                    inputs.forEach(i => i.checked = false);
                    this.checked = true;
                }
                console.log("Multiple choice option selected:", this.value);
            });
        });
    });
}

function initializeDragAndDrop() {
    console.log("Initializing drag and drop");
    const dragItems = document.querySelectorAll('.drag-item');
    const dropZones = document.querySelectorAll('.drop-zone');

    dragItems.forEach(item => {
        item.addEventListener('dragstart', dragStart);
        item.addEventListener('dragend', dragEnd);
        item.addEventListener('touchstart', touchStart, { passive: false });
        item.addEventListener('touchmove', touchMove, { passive: false });
        item.addEventListener('touchend', touchEnd, { passive: false });
    });

    dropZones.forEach(zone => {
        zone.addEventListener('dragover', dragOver);
        zone.addEventListener('dragenter', dragEnter);
        zone.addEventListener('dragleave', dragLeave);
        zone.addEventListener('drop', drop);
    });
}

function dragStart(e) {
    console.log('Drag started', e.target);
    const dragItem = e.target.closest('.drag-item');
    if (!dragItem) {
        console.error('No .drag-item parent found for dragged element:', e.target);
        return;
    }
    const itemId = dragItem.dataset.itemId;
    if (!itemId) {
        console.error('No data-item-id found on dragged element:', dragItem);
        return;
    }
    e.dataTransfer.setData('text/plain', itemId);
    console.log('Set data transfer:', itemId);
    setTimeout(() => {
        dragItem.classList.add('dragging');
    }, 0);
}

function dragEnd(e) {
    console.log('Drag ended');
    e.target.classList.remove('dragging');
}

function dragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('drag-over');
}

function dragEnter(e) {
    e.preventDefault();
    e.currentTarget.classList.add('drag-over');
}

function dragLeave(e) {
    e.currentTarget.classList.remove('drag-over');
}

function drop(e) {
    console.log('Drop event', e);
    e.preventDefault();
    e.currentTarget.classList.remove('drag-over');

    const id = e.dataTransfer.getData('text/plain');
    console.log('Retrieved data transfer:', id);
    const draggable = document.querySelector(`.drag-item[data-item-id="${id}"]`);
    console.log('Draggable element:', draggable);

    if (!draggable) {
        console.error('Draggable element not found for id:', id);
        return;
    }

    if (e.currentTarget.classList.contains('drop-zone')) {
        const existingItem = e.currentTarget.querySelector('.drag-item');
        if (existingItem) {
            const originalPosition = document.querySelector('.drag-items');
            if (originalPosition) {
                originalPosition.appendChild(existingItem);
            } else {
                console.error('Original position element not found');
            }
        }
        try {
            e.currentTarget.appendChild(draggable);
            console.log('Item dropped successfully');
        } catch (error) {
            console.error('Error appending draggable:', error);
        }
    }

    draggable.classList.remove('dragging');
    updateDropZoneStyles();
}

function touchStart(e) {
    if (e.touches.length === 1) {
        e.preventDefault();
        this.classList.add('dragging');
        this.style.position = 'absolute';
        this.style.zIndex = 1000;
        moveAt(this, e.touches[0]);
    }
}

function touchMove(e) {
    if (e.touches.length === 1) {
        e.preventDefault();
        moveAt(this, e.touches[0]);
    }
}

function touchEnd(e) {
    this.classList.remove('dragging');
    this.style.position = '';
    this.style.zIndex = '';

    const dropZone = document.elementFromPoint(
        e.changedTouches[0].clientX,
        e.changedTouches[0].clientY
    );

    if (dropZone && dropZone.classList.contains('drop-zone')) {
        const existingItem = dropZone.querySelector('.drag-item');
        if (existingItem) {
            const originalPosition = document.querySelector('.drag-items');
            originalPosition.appendChild(existingItem);
        }
        dropZone.appendChild(this);
        console.log('Item dropped via touch');
    } else {
        const originalPosition = document.querySelector('.drag-items');
        originalPosition.appendChild(this);
        console.log('Item returned to original position');
    }
    updateDropZoneStyles();
}

function moveAt(element, touch) {
    const rect = element.getBoundingClientRect();
    element.style.left = touch.clientX - rect.width / 2 + 'px';
    element.style.top = touch.clientY - rect.height / 2 + 'px';
}

function initializeSimulations() {
    console.log("Initializing simulations");
    const simulationContainers = document.querySelectorAll('.simulation-container');
    console.log("Simulation containers found:", simulationContainers.length);

    simulationContainers.forEach(container => {
        const questionId = container.dataset.questionId;
        console.log("Processing simulation for question ID:", questionId);
        
        const terminalElement = container.querySelector('.terminal');
        const expectedCommandsElement = container.querySelector('.expected-commands');
        
        console.log("Terminal element:", terminalElement);
        console.log("Expected commands:", expectedCommandsElement ? expectedCommandsElement.textContent : 'Not found');

        if (!terminalElement) {
            console.error("Terminal element not found for question ID:", questionId);
            return;
        }

        try {
            if (typeof Terminal === 'undefined') {
                console.error("Terminal object not found. Make sure xterm.js is loaded properly.");
                return;
            }

            const term = new Terminal({
                cursorBlink: true,
                theme: {
                    background: '#000000',
                    foreground: '#ffffff'
                },
                rows: 24,
                cols: 80,
                scrollback: 1000,
                convertEol: true
            });

            console.log("Terminal instance created");

            term.open(terminalElement);
            console.log("Terminal opened");
            
            if (typeof FitAddon !== 'undefined') {
                const fitAddon = new FitAddon.FitAddon();
                term.loadAddon(fitAddon);
                fitAddon.fit();
                console.log("Terminal fitted");
            } else {
                console.warn("FitAddon not available. Terminal size might not be optimal.");
            }
            
            if (term.element) {
                term.element.style.padding = '10px';
            }
            
            let currentLine = '';
            let commandHistory = [];
            let historyIndex = -1;
            let currentPrompt = 'C:\\> ';

            function setPrompt(newPrompt) {
                currentPrompt = newPrompt;
                term.write('\r\n' + currentPrompt);
            }

            fetch('/api/get_initial_state/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ question_id: questionId })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Initial state received:", data);
                setPrompt(data.prompt || 'C:\\> ');
            })
            .catch(error => {
                console.error("Error fetching initial state:", error);
                setPrompt('C:\\> ');
            });

            term.onKey(({ key, domEvent }) => {
                const printable = !domEvent.altKey && !domEvent.ctrlKey && !domEvent.metaKey;

                if (domEvent.keyCode === 13) { // Enter key
                    term.write('\r\n');
                    if (currentLine.trim() !== '') {
                        executeCommand(currentLine, questionId, term, container, setPrompt);
                        commandHistory.unshift(currentLine);
                        historyIndex = -1;
                    }
                    currentLine = '';
                } else if (domEvent.keyCode === 8) { // Backspace
                    if (currentLine.length > 0) {
                        currentLine = currentLine.slice(0, -1);
                        term.write('\b \b');
                    }
                } else if (domEvent.keyCode === 38) { // Up arrow
                    if (historyIndex < commandHistory.length - 1) {
                        historyIndex++;
                        currentLine = commandHistory[historyIndex];
                        term.write('\r' + currentPrompt + ' '.repeat(term.cols - currentPrompt.length));
                        term.write('\r' + currentPrompt + currentLine);
                    }
                } else if (domEvent.keyCode === 40) { // Down arrow
                    if (historyIndex > -1) {
                        historyIndex--;
                        if (historyIndex === -1) {
                            currentLine = '';
                        } else {
                            currentLine = commandHistory[historyIndex];
                        }
                        term.write('\r' + currentPrompt + ' '.repeat(term.cols - currentPrompt.length));
                        term.write('\r' + currentPrompt + currentLine);
                    }
                } else if (printable) {
                    currentLine += key;
                    term.write(key);
                }
            });
            
            console.log("Event listener added to terminal");

            container.dataset.commandHistory = JSON.stringify(commandHistory);

            window.addEventListener('resize', () => {
                if (typeof FitAddon !== 'undefined') {
                    const fitAddon = new FitAddon.FitAddon();
                    term.loadAddon(fitAddon);
                    fitAddon.fit();
                }
            });

            if (expectedCommandsElement) {
                const expectedCommands = expectedCommandsElement.textContent.split('\n').filter(cmd => cmd.trim() !== '');
                console.log("Expected commands:", expectedCommands);
                container.dataset.expectedCommands = JSON.stringify(expectedCommands);
            }

        } catch (error) {
            console.error("Error initializing terminal:", error);
        }
    });
}

function populateQuestionNavigation(totalQuestions) {
    console.log("Populating question navigation");
    const navContainer = document.getElementById('question-navigation');
    navContainer.innerHTML = ''; // Clear existing buttons
    for (let i = 0; i < totalQuestions; i++) {
        const button = document.createElement('button');
        button.className = 'question-nav-button';
        button.textContent = i + 1;
        button.dataset.index = i.toString();
        button.style.backgroundColor = '#007bff'; // Initial blue color
        button.addEventListener('click', () => {
            if (!isLoading) {
                storeAnswer(currentQuestionIndex);
                currentQuestionIndex = i;
                loadQuestion(currentQuestionIndex);
            }
        });
        navContainer.appendChild(button);
    }
    console.log(`Populated ${totalQuestions} navigation buttons`);
}

function updateQuestionNavigation(currentIndex) {
    console.log("Updating question navigation");
    const buttons = document.querySelectorAll('.question-nav-button');
    buttons.forEach((button, index) => {
        button.classList.remove('current');
        if (index === currentIndex) {
            button.classList.add('current');
        }
        if (answers[button.dataset.questionId] !== undefined) {
            button.classList.add('answered');
        } else {
            button.classList.remove('answered');
        }
    });
}

function executeCommand(command, questionId, term, container, setPrompt) {
    console.log(`Executing command: ${command} for question ${questionId}`);
    fetch('/execute-command/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            command: command,
            question_id: questionId
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Full server response:", data);
        if (data.printed_output) {
            console.log("Writing printed output:", data.printed_output);
            term.writeln(data.printed_output);
        }
        if (data.error) {
            console.error("Error from server:", data.error);
            term.writeln(`Error: ${data.error}`);
        }
        console.log("Setting new prompt:", data.prompt);
        setPrompt(data.prompt || 'C:\\> ');
        
        let commandHistory = JSON.parse(container.dataset.commandHistory || '[]');
        commandHistory.unshift(command);
        container.dataset.commandHistory = JSON.stringify(commandHistory);

        if (data.current_directory) {
            container.dataset.currentDirectory = data.current_directory;
        }

        // Check if the command matches the expected commands
        const expectedCommands = JSON.parse(container.dataset.expectedCommands || '[]');
        if (expectedCommands.length > 0 && command.trim() === expectedCommands[0].trim()) {
            expectedCommands.shift();
            container.dataset.expectedCommands = JSON.stringify(expectedCommands);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        term.writeln(`Error executing command: ${error}`);
        setPrompt('C:\\> ');
    });
}

function initializeMatching() {
    console.log("Initializing matching");
    const matchItems = document.querySelectorAll('.match-item');
    let selectedItem = null;

    matchItems.forEach(item => {
        item.addEventListener('click', function() {
            if (selectedItem === null) {
                selectedItem = this;
                this.classList.add('selected');
                console.log('Item selected:', this.textContent);
            } else {
                if (this !== selectedItem) {
                    if (this.dataset.itemId === selectedItem.dataset.itemId) {
                        this.classList.add('matched');
                        selectedItem.classList.add('matched');
                        console.log('Items matched:', selectedItem.textContent, this.textContent);
                    } else {
                        console.log('Mismatch:', selectedItem.textContent, this.textContent);
                        setTimeout(() => {
                            this.classList.add('error');
                            selectedItem.classList.add('error');
                        }, 0);
                        setTimeout(() => {
                            this.classList.remove('error');
                            selectedItem.classList.remove('error');
                        }, 1000);
                    }
                }
                selectedItem.classList.remove('selected');
                selectedItem = null;
            }
        });
    });
}

function initializeFillInTheBlank() {
    console.log("Initializing fill in the blank questions");
    const fibQuestions = document.querySelectorAll('.question[data-question-type="FIB"]');
    fibQuestions.forEach(question => {
        const inputs = question.querySelectorAll('input[type="text"]');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                console.log('Fill in the blank input changed:', this.value);
                // You can add any specific behavior for FIB questions here
            });
        });
    });
}

function updateDropZoneStyles() {
    console.log("Updating drop zone styles");
    const dropZones = document.querySelectorAll('.drop-zone');
    dropZones.forEach(zone => {
        if (zone.querySelector('.drag-item')) {
            zone.classList.add('filled');
        } else {
            zone.classList.remove('filled');
        }
    });
}

function resetDragItems() {
    console.log("Resetting drag items");
    const dragItems = document.querySelectorAll('.drag-item');
    const dragItemsContainer = document.querySelector('.drag-items');

    dragItems.forEach(item => {
        if (item.parentElement.classList.contains('drop-zone')) {
            dragItemsContainer.appendChild(item);
        }
    });
    updateDropZoneStyles();
}

window.onerror = function(message, source, lineno, colno, error) {
    console.error('An error occurred:', message, 'at', source, 'line', lineno, 'column', colno);
    return false;
};

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('test-form')) {
        console.log("Test form found, initializing test taking");
        initializeTestTaking();
    } else {
        console.log("Test form not found, skipping test taking initialization");
    }
});

console.log("test_taking.js fully loaded and initialized");