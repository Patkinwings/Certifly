console.log("test_taking.js loaded");

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    initializeDragAndDrop();
    initializeSimulations();
    initializeMatching();
    initializeTimer();
    
    // Manual terminal initialization for debugging
    try {
        var term = new Terminal();
        var terminalElement = document.getElementById('terminal-1');
        if (terminalElement) {
            term.open(terminalElement);
            term.write('Hello from terminal\r\n');
            console.log("Manual terminal initialization successful");
        } else {
            console.error("Terminal element not found");
        }
    } catch (error) {
        console.error("Error in manual terminal initialization:", error);
    }

    // Check for simulation container
    var simulationContainer = document.querySelector('.simulation-container');
    console.log("Simulation container:", simulationContainer);
});

function initializeDragAndDrop() {
    console.log("Initializing drag and drop");
    const dragItems = document.querySelectorAll('.drag-item');
    const dropZones = document.querySelectorAll('.drop-zone');

    dragItems.forEach(item => {
        item.addEventListener('dragstart', dragStart);
        item.addEventListener('dragend', dragEnd);
    });

    dropZones.forEach(zone => {
        zone.addEventListener('dragover', dragOver);
        zone.addEventListener('dragenter', dragEnter);
        zone.addEventListener('dragleave', dragLeave);
        zone.addEventListener('drop', drop);
    });
}

function dragStart(e) {
    e.dataTransfer.setData('text/plain', e.target.dataset.itemId);
    setTimeout(() => {
        e.target.classList.add('hide');
    }, 0);
}

function dragEnd(e) {
    e.target.classList.remove('hide');
}

function dragOver(e) {
    e.preventDefault();
}

function dragEnter(e) {
    e.preventDefault();
    e.target.classList.add('drag-over');
}

function dragLeave(e) {
    e.target.classList.remove('drag-over');
}

function drop(e) {
    e.target.classList.remove('drag-over');

    const id = e.dataTransfer.getData('text/plain');
    const draggable = document.querySelector(`[data-item-id="${id}"]`);

    e.target.appendChild(draggable);

    draggable.classList.remove('hide');
}

function initializeSimulations() {
    console.log("Initializing simulations");
    const simulationContainers = document.querySelectorAll('.simulation-container');
    console.log("Simulation containers found:", simulationContainers.length);
    
    simulationContainers.forEach(container => {
        const questionId = container.closest('.question').dataset.questionId;
        console.log("Processing simulation for question ID:", questionId);
        
        const terminalElement = container.querySelector('.terminal');
        const inputElement = container.querySelector('.command-input');
        
        console.log("Terminal element:", terminalElement);
        console.log("Input element:", inputElement);

        if (!terminalElement || !inputElement) {
            console.error("Terminal or input element not found for question ID:", questionId);
            return;
        }

        try {
            const term = new Terminal({
                cursorBlink: true,
                theme: {
                    background: '#000000',
                    foreground: '#ffffff'
                }
            });

            console.log("Terminal instance created");

            term.open(terminalElement);
            console.log("Terminal opened");
            
            if (typeof term.fit === 'function') {
                term.fit();
                console.log("Terminal fitted");
            } else {
                console.warn("Term.fit is not available. Make sure you've included the 'fit' addon.");
            }
            
            term.write('Simulator Ready\r\n$ ');
            console.log("Initial prompt written to terminal");

            inputElement.addEventListener('keyup', function(e) {
                if (e.key === 'Enter') {
                    const command = this.value.trim();
                    if (command) {
                        console.log("Command entered:", command);
                        term.write(`\r\n$ ${command}\r\n`);
                        executeCommand(command, questionId, term);
                        this.value = '';
                    }
                }
            });
            
            console.log("Event listener added to input element");
        } catch (error) {
            console.error("Error initializing terminal:", error);
        }
    });
}

function executeCommand(command, questionId, term) {
    console.log(`Executing command: ${command} for question ${questionId}`);
    fetch('/execute-command/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            command: command,
            simulation_id: questionId
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Command result:", data.result);
        term.write(`${data.result}\r\n$ `);
    })
    .catch(error => {
        console.error('Error:', error);
        term.write(`Error executing command: ${error}\r\n$ `);
    });
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

document.getElementById('test-form').addEventListener('submit', function(e) {
    e.preventDefault();
    console.log("Form submitted");
    const formData = new FormData(this);
    const answers = {};

    // Process multiple choice and fill in the blank answers
    for (let [key, value] of formData.entries()) {
        if (key.startsWith('question_')) {
            const questionId = key.split('_')[1];
            if (Array.isArray(answers[questionId])) {
                answers[questionId].push(value);
            } else {
                answers[questionId] = [value];
            }
        }
    }

    // Process drag and drop answers
    document.querySelectorAll('.drag-drop-container').forEach(container => {
        const questionId = container.closest('.question').dataset.questionId;
        const dropZones = container.querySelectorAll('.drop-zone');
        answers[questionId] = Array.from(dropZones).map(zone => {
            const item = zone.querySelector('.drag-item');
            return item ? item.dataset.itemId : null;
        });
    });

    // Process matching answers
    document.querySelectorAll('.matching-container').forEach(container => {
        const questionId = container.closest('.question').dataset.questionId;
        const matchedPairs = [];
        const leftItems = container.querySelectorAll('.left-items .match-item.matched');
        leftItems.forEach(item => {
            const rightItem = container.querySelector(`.right-items .match-item.matched[data-item-id="${item.dataset.itemId}"]`);
            if (rightItem) {
                matchedPairs.push([item.dataset.itemId, rightItem.dataset.itemId]);
            }
        });
        answers[questionId] = matchedPairs;
    });

    // Process simulation answers
    document.querySelectorAll('.simulation-container').forEach(container => {
        const questionId = container.closest('.question').dataset.questionId;
        const terminalElement = container.querySelector('.terminal');
        answers[questionId] = terminalElement.innerText;
    });

    console.log("Answers collected:", answers);

    // Send answers to server
    fetch('/submit-test/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            test_id: this.dataset.testId,
            answers: answers
        })
    })
    .then(response => response.json())
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