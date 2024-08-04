console.log("test_taking.js loaded");

let answers = {};
let testDuration;
let endTime;

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    
    const testContainer = document.getElementById('question-container');
    if (testContainer) {
        initializeTestTaking();
    } else {
        initializeQuestionCreation();
    }
});

function initializeTestTaking() {
    let currentQuestionIndex = 0;
    const testForm = document.getElementById('test-form');
    if (!testForm) {
        console.error('Test form not found');
        return;
    }
    const testId = parseInt(testForm.dataset.testId);
    const totalQuestions = parseInt(testForm.dataset.totalQuestions);
    testDuration = parseInt(testForm.dataset.duration, 10);
    
    if (isNaN(testId) || isNaN(totalQuestions) || isNaN(testDuration)) {
        console.error('Invalid test data');
        return;
    }

    loadQuestion(currentQuestionIndex);
    initializeTimer();

    testForm.addEventListener('click', function(event) {
        if (event.target.id === 'prev-question') {
            if (currentQuestionIndex > 0) {
                storeAnswer(currentQuestionIndex);
                currentQuestionIndex--;
                loadQuestion(currentQuestionIndex);
            }
        } else if (event.target.id === 'next-question') {
            if (currentQuestionIndex < totalQuestions - 1) {
                storeAnswer(currentQuestionIndex);
                currentQuestionIndex++;
                loadQuestion(currentQuestionIndex);
            }
        } else if (event.target.id === 'finish-test') {
            storeAnswer(currentQuestionIndex);
            finishTest();
        }
    });
}

function loadQuestion(index) {
    const testForm = document.getElementById('test-form');
    if (!testForm) {
        console.error('Test form not found');
        return;
    }
    const testId = parseInt(testForm.dataset.testId);
    const totalQuestions = parseInt(testForm.dataset.totalQuestions);
    
    if (isNaN(testId) || isNaN(totalQuestions)) {
        console.error('Invalid test data');
        return;
    }
    
    fetch(`/test/${testId}/question/${index}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const testContainer = document.getElementById('question-container');
            if (!testContainer) {
                console.error('Question container not found');
                return;
            }
            testContainer.innerHTML = `
                <h2>Question ${index + 1}</h2>
                <p>${data.text}</p>
            `;
            if (data.image) {
                testContainer.innerHTML += `<img src="${data.image}" alt="Question Image">`;
            }
            renderQuestionType(data);

            // Update navigation buttons
            const prevButton = document.getElementById('prev-question');
            const nextButton = document.getElementById('next-question');
            const finishButton = document.getElementById('finish-test');

            if (prevButton) prevButton.style.display = 'inline';
            if (nextButton) nextButton.style.display = 'inline';
            if (finishButton) finishButton.style.display = index === totalQuestions - 1 ? 'inline' : 'none';

            // Ensure the timer is always visible
            const timerElement = document.getElementById('test-timer');
            if (timerElement && testContainer.firstChild) {
                testContainer.insertBefore(timerElement, testContainer.firstChild);
            }

            // Restore previously stored answer
            if (answers[index]) {
                restoreAnswer(data, answers[index]);
            }
        })
        .catch(error => {
            console.error('Error loading question:', error);
        });
}

function renderQuestionType(data) {
    const testContainer = document.getElementById('question-container');
    let questionHtml = '';
    switch(data.question_type) {
        case 'MC':
            questionHtml = renderMultipleChoice(data);
            break;
        case 'DD':
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
    }
    testContainer.innerHTML += questionHtml;
    
    if (data.question_type === 'MC') {
        initializeMultipleChoice();
    } else if (data.question_type === 'DD') {
        initializeDragAndDrop();
    } else if (data.question_type === 'MAT') {
        initializeMatching();
    } else if (data.question_type === 'FIB') {
        initializeFillInTheBlank();
    } else if (data.question_type === 'SIM') {
        initializeSimulations();
    }
}

function renderMultipleChoice(data) {
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
    let html = '<div class="drag-drop-container">';
    html += '<div class="drag-items">';
    data.drag_drop_items.forEach(item => {
        html += `<div class="drag-item" draggable="true" data-item-id="${item.id}">${item.text}</div>`;
    });
    html += '</div>';
    html += '<div class="drop-zones">';
    data.drag_drop_zones.forEach(zone => {
        html += `<div class="drop-zone" data-zone-id="${zone.id}">${zone.text}</div>`;
    });
    html += '</div></div>';
    return html;
}

function renderMatching(data) {
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
    let html = '<div class="fill-in-the-blank-container">';
    data.fill_in_the_blanks.forEach((blank, index) => {
        html += `<input type="text" name="blank_${index}" placeholder="Fill in the blank">`;
    });
    html += '</div>';
    return html;
}

function renderSimulation(data) {
    return `
        <div class="simulation-container" data-question-id="${data.id}">
            <div class="terminal"></div>
        </div>
    `;
}

function storeAnswer(index) {
    const answer = getAnswerForCurrentQuestion();
    answers[index] = answer;
}

function restoreAnswer(data, answer) {
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
    }
}

function getAnswerForCurrentQuestion() {
    const questionContainer = document.getElementById('question-container');
    const questionType = questionContainer.querySelector('.question').dataset.questionType;
    
    switch (questionType) {
        case 'MC':
            return Array.from(questionContainer.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value);
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
            return JSON.parse(container.dataset.commandHistory || '[]');
        default:
            console.warn(`Unknown question type: ${questionType}`);
            return null;
    }
}

function finishTest() {
    const testId = document.getElementById('test-form').dataset.testId;
    fetch(`/test/${testId}/finish/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(answers)
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              window.location.href = data.redirect_url;
          } else {
              console.error('Error finishing test:', data.error);
          }
      });
}

function initializeQuestionCreation() {
    const questionTypeSelect = document.getElementById('id_question_type');
    const answerFormset = document.getElementById('answer-formset');
    const dragDropFormset = document.getElementById('drag-drop-formset');
    const fibFormset = document.getElementById('fill-in-the-blank-formset');

    if (questionTypeSelect) {
        function toggleFormsets() {
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
                    this.checked = true;}
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
        setTimeout(() => {dragItem.classList.add('dragging');
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
    
    function updateTimer(endTime) {
        const timerElement = document.getElementById('test-timer');
    
        function updateDisplay() {
            const now = new Date().getTime();
            const distance = endTime - now;
    
            if (distance < 0) {
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
        if (isNaN(testDuration)) {
            console.error("Invalid test duration");
            return;
        }
        endTime = new Date().getTime() + testDuration * 60 * 1000;
        updateTimer(endTime);
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

    document.addEventListener('DOMContentLoaded', function() {
        if (document.getElementById('test-form')) {
            initializeTestTaking();
        }
    });
    
    console.log("test_taking.js fully loaded and initialized");

