console.log("test_taking.js loaded");

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    
    if (document.querySelector('.question[data-question-type="MC"]')) {
        initializeMultipleChoice();
    }
    
    if (document.querySelector('.drag-item')) {
        initializeDragAndDrop();
    }
    
    if (document.querySelector('.simulation-container')) {
        initializeSimulations();
    }
    
    if (document.querySelector('.match-item')) {
        initializeMatching();
    }
    
    if (document.querySelector('.question[data-question-type="FIB"]')) {
        initializeFillInTheBlank();
    }
    
    if (document.getElementById('test-form')) {
        initializeTimer();
    }

    const testForm = document.getElementById('test-form');
    if (testForm) {
        const resetButton = document.createElement('button');
        resetButton.type = 'button';
        resetButton.textContent = 'Reset Drag and Drop';
        resetButton.addEventListener('click', resetDragItems);
        testForm.insertBefore(resetButton, testForm.querySelector('button[type="submit"]'));
    }

    initializeMobileDragAndDrop();

    // Add this part for the question type selector
    const questionTypeSelect = document.getElementById('id_question_type');
    if (questionTypeSelect) {
        const answerFormset = document.getElementById('answer-formset');
        const dragDropFormset = document.getElementById('drag-drop-formset');

        function toggleFormsets() {
            if (questionTypeSelect.value === 'MC') {
                answerFormset.style.display = 'block';
                dragDropFormset.style.display = 'none';
            } else if (questionTypeSelect.value === 'DD') {
                answerFormset.style.display = 'none';
                dragDropFormset.style.display = 'block';
            } else {
                answerFormset.style.display = 'none';
                dragDropFormset.style.display = 'none';
            }
        }

        questionTypeSelect.addEventListener('change', toggleFormsets);
        toggleFormsets();
    }

    // Add this part for handling image uploads
    const questionForm = document.getElementById('question-form');
    if (questionForm) {
        questionForm.addEventListener('submit', handleQuestionFormSubmit);
    }
});

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
    } else {
        const originalPosition = document.querySelector('.drag-items');
        originalPosition.appendChild(this);
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
        
        console.log("Terminal element:", terminalElement);

        if (!terminalElement) {
            console.error("Terminal element not found for question ID:", questionId);
            return;
        }

        try {
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
            
            if (typeof fit !== 'undefined' && typeof fit.fit === 'function') {
                fit.fit(term);
                console.log("Terminal fitted");
            } else {
                console.warn("Term.fit is not available. Make sure you've included the 'fit' addon.");
            }
            
            if (term.element) {
                term.element.style.padding = '10px';
            }
            
            term.write('Simulator Ready\r\n$ ');
            console.log("Initial prompt written to terminal");

            let currentLine = '';
            let commandHistory = [];

            term.onKey(({ key, domEvent }) => {
                const printable = !domEvent.altKey && !domEvent.ctrlKey && !domEvent.metaKey;

                if (domEvent.keyCode === 13) { // Enter key
                    term.write('\r\n');
                    executeCommand(currentLine, questionId, term, container);
                    commandHistory.push(currentLine);
                    currentLine = '';
                } else if (domEvent.keyCode === 8) { // Backspace
                    if (currentLine.length > 0) {
                        currentLine = currentLine.slice(0, -1);
                        term.write('\b \b');
                    }
                } else if (printable) {
                    currentLine += key;
                    term.write(key);
                }
            });
            
            console.log("Event listener added to terminal");

            container.dataset.commandHistory = JSON.stringify(commandHistory);

            window.addEventListener('resize', () => {
                if (typeof fit !== 'undefined' && typeof fit.fit === 'function') {
                    fit.fit(term);
                }
            });
        } catch (error) {
            console.error("Error initializing terminal:", error);
        }
    });
}

function executeCommand(command, questionId, term, container) {
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
        console.log("Raw data received from server:", data);
        if (data.printed_output) {
            console.log("Writing printed output:", data.printed_output);
            term.writeln(data.printed_output);
        }
        if (data.result !== undefined && data.result !== true) {
            console.log("Writing result:", data.result);
            term.writeln(data.result.toString());
        }
        const prompt = data.current_directory ? `${data.current_directory}>` : 'C:\\>';
        console.log("Writing command prompt:", prompt);
        term.write(`\r\n${prompt}`);
        
        // Update command history
        container.dataset.commandHistory = JSON.stringify([...JSON.parse(container.dataset.commandHistory || '[]'), command]);
    })
    .catch(error => {
        console.error('Error:', error);
        term.writeln(`Error executing command: ${error}`);
        term.write('\r\nC:\\>');
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
            } else {
                if (this !== selectedItem) {
                    if (this.dataset.itemId === selectedItem.dataset.itemId) {
                        this.classList.add('matched');
                        selectedItem.classList.add('matched');
                    } else {
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
        const input = question.querySelector('input[type="text"]');
        input.addEventListener('input', function() {
            // You can add any specific behavior for FIB questions here
        });
    });
}

document.getElementById('test-form').addEventListener('submit', function(e) {
    e.preventDefault();
    console.log("Form submitted");
    
    if (!validateForm()) {
        alert('Please answer all questions before submitting.');
        return;
    }

    const formData = new FormData(this);
    const answers = {};

    document.querySelectorAll('.question[data-question-type="MC"]').forEach(question => {
        const questionId = question.dataset.questionId;
        const selectedInputs = question.querySelectorAll('input:checked');
        answers[questionId] = Array.from(selectedInputs).map(input => input.value);
    });

    document.querySelectorAll('.question[data-question-type="FIB"]').forEach(question => {
        const questionId = question.dataset.questionId;
        const input = question.querySelector('input[type="text"]');
        answers[questionId] = [input.value];
    });

    document.querySelectorAll('.question[data-question-type="DD"]').forEach(question => {
        const questionId = question.dataset.questionId;
        const dropZones = question.querySelectorAll('.drop-zone');
        answers[questionId] = {};
        dropZones.forEach(zone => {
            const zoneId = zone.dataset.zoneId;
            const item = zone.querySelector('.drag-item');
            answers[questionId][zoneId] = item ? item.dataset.itemId : null;
        });
    });

    document.querySelectorAll('.question[data-question-type="SIM"]').forEach(question => {
        const questionId = question.dataset.questionId;
        const container = question.querySelector('.simulation-container');
        const commandHistory = JSON.parse(container.dataset.commandHistory || '[]');
        answers[questionId] = commandHistory
    });

    console.log("Form data before submission:", JSON.stringify(answers));

    fetch('/test/' + this.dataset.testId + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            answers: answers,
            start_time: this.dataset.startTime
        })
    })
    .then(response => {
        console.log('Server response:', response);
        return response.json();
    })
    .then(data => {
        if (data.success) {
            console.log("Test submitted successfully");
            window.location.href = data.redirect_url;
        } else {
            console.error("Error submitting test:", data.error);
            alert('Error submitting test. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error submitting test. Please try again.');
    });
});

function updateTimer(endTime) {
    const timerElement = document.getElementById('test-timer');

    function updateDisplay() {
        const now = new Date().getTime();
        const distance = endTime - now;

        if (distance < 0) {
            clearInterval(timerInterval);
            timerElement.innerHTML = "Time's up!";
            document.getElementById('test-form').submit();
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
    const testForm = document.getElementById('test-form');
    if (testForm) {
        const testDuration = parseInt(testForm.dataset.duration, 10);
        const endTime = new Date().getTime() + testDuration * 60 * 1000;
        updateTimer(endTime);
    } else {
        console.error("Test form not found");
    }
}

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

function resetDragItems() {
    const dragItems = document.querySelectorAll('.drag-item');
    const dragItemsContainer = document.querySelector('.drag-items');

    dragItems.forEach(item => {
        if (item.parentElement.classList.contains('drop-zone')) {
            dragItemsContainer.appendChild(item);
        }
    });
    updateDropZoneStyles();
}

function initializeMobileDragAndDrop() {
    const dragItems = document.querySelectorAll('.drag-item');
    const dropZones = document.querySelectorAll('.drop-zone');

    let draggedItem = null;

    dragItems.forEach(item => {
        item.addEventListener('touchstart', function(e) {
            draggedItem = this;
            this.classList.add('dragging');
        }, { passive: false });

        item.addEventListener('touchend', function(e) {
            this.classList.remove('dragging');
            draggedItem = null;
        });
    });

    dropZones.forEach(zone => {
        zone.addEventListener('touchend', function(e) {
            e.preventDefault();
            if (draggedItem) {
                const existingItem = this.querySelector('.drag-item');
                if (existingItem) {
                    const dragItemsContainer = document.querySelector('.drag-items');
                    dragItemsContainer.appendChild(existingItem);
                }
                this.appendChild(draggedItem);
                draggedItem.classList.remove('dragging');
                draggedItem = null;
                updateDropZoneStyles();
            }
        });
    });
}

function updateDropZoneStyles() {
    const dropZones = document.querySelectorAll('.drop-zone');
    dropZones.forEach(zone => {
        if (zone.querySelector('.drag-item')) {
            zone.classList.add('filled');
        } else {
            zone.classList.remove('filled');
        }
    });
}

window.onerror = function(message, source, lineno, colno, error) {
    console.error('An error occurred:', message, 'at', source, 'line', lineno, 'column', colno);
    return false;
};

function validateForm() {
    let isValid = true;
    const questions = document.querySelectorAll('.question');

    console.log(`Validating ${questions.length} questions`);

    questions.forEach(question => {
        const questionType = question.dataset.questionType;
        const questionId = question.dataset.questionId;
        
        console.log(`Validating question ${questionId} of type ${questionType}`);
        
        switch (questionType) {
            case 'MC':
                const checkedInputs = question.querySelectorAll('input:checked');
                if (checkedInputs.length === 0) {
                    isValid = false;
                    question.classList.add('unanswered');
                    console.log(`Question ${questionId} is unanswered (MC)`);
                } else {
                    question.classList.remove('unanswered');
                    console.log(`Question ${questionId} is answered (MC)`);
                }
                break;
            case 'FIB':
                const input = question.querySelector('input[type="text"]');
                if (!input.value.trim()) {
                    isValid = false;
                    question.classList.add('unanswered');
                    console.log(`Question ${questionId} is unanswered (FIB)`);
                } else {
                    question.classList.remove('unanswered');
                    console.log(`Question ${questionId} is answered (FIB)`);
                }
                break;
            case 'DD':
                const filledDropZones = question.querySelectorAll('.drop-zone .drag-item');
                if (filledDropZones.length === 0) {
                    isValid = false;
                    question.classList.add('unanswered');
                    console.log(`Question ${questionId} is unanswered (DD)`);
                } else {
                    question.classList.remove('unanswered');
                    console.log(`Question ${questionId} is answered (DD)`);
                }
                break;
            case 'MAT':
                const matchedItems = question.querySelectorAll('.match-item.matched');
                if (matchedItems.length === 0) {
                    isValid = false;
                    question.classList.add('unanswered');
                    console.log(`Question ${questionId} is unanswered (MAT)`);
                } else {
                    question.classList.remove('unanswered');
                    console.log(`Question ${questionId} is answered (MAT)`);
                }
                break;
            case 'SIM':
                const simulationContainer = question.querySelector('.simulation-container');
                if (simulationContainer) {
                    const commandHistory = JSON.parse(simulationContainer.dataset.commandHistory || '[]');
                    if (commandHistory.length === 0) {
                        console.log(`Question ${questionId} has no commands entered (SIM)`);
                    } else {
                        console.log(`Question ${questionId} has ${commandHistory.length} commands entered (SIM)`);
                    }
                } else {
                    console.warn(`No simulation container found for question ${questionId}`);
                }
                // Always consider SIM questions as answered
                question.classList.remove('unanswered');
                console.log(`Question ${questionId} is considered answered (SIM)`);
                break;
            default:
                console.warn(`Unknown question type: ${questionType} for question ${questionId}`);
        }
    });

    console.log(`Form validation result: ${isValid ? 'Valid' : 'Invalid'}`);
    return isValid;
}

function handleQuestionFormSubmit(event) {
    event.preventDefault();
    console.log("Question form submitted");

    const form = event.target;
    const formData = new FormData(form);

    // First, create the question without the image
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Question created successfully");
            if (data.image_pending) {
                uploadQuestionImage(data.question_id, formData.get('image'));
            } else {
                window.location.href = data.redirect_url || '/dashboard/';
            }
        } else {
            console.error("Error creating question:", data.error);
            alert('Error creating question. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error creating question. Please try again.');
    });
}

function uploadQuestionImage(questionId, imageFile) {
    if (!imageFile) {
        console.log("No image file to upload");
        return;
    }

    const formData = new FormData();
    formData.append('image', imageFile);

    fetch(`/upload-question-image/${questionId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Image uploaded successfully");
            window.location.href = '/dashboard/';
        } else {
            console.error("Error uploading image:", data.error);
            alert('Error uploading image. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading image. Please try again.');
    });
}

console.log("test_taking.js fully loaded and initialized");