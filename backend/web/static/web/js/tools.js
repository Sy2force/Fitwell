/* Tools Logic: BMI, Macros, Stopwatch, Timer */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize tabs if needed
});

/* --- BMI Calculator --- */
function calculateBMI() {
    const heightCm = parseFloat(document.getElementById('bmi-height').value);
    const weightKg = parseFloat(document.getElementById('bmi-weight').value);

    if (!heightCm || !weightKg) {
        alert(window.toolsConfig.alertMissingData || "Veuillez entrer votre taille et poids.");
        return;
    }

    const heightM = heightCm / 100;
    const bmi = weightKg / (heightM * heightM);
    
    const bmiValueElement = document.getElementById('bmi-value');
    const bmiCategoryElement = document.getElementById('bmi-category');
    const resultContainer = document.getElementById('bmi-result');

    if(bmiValueElement) bmiValueElement.innerText = bmi.toFixed(1);
    
    let category = "";
    let colorClass = "text-white";

    if (bmi < 18.5) {
        category = window.toolsConfig.bmiUnderweight || "Maigreur";
        colorClass = "text-yellow-500";
    } else if (bmi < 25) {
        category = window.toolsConfig.bmiNormal || "Corpulence Normale";
        colorClass = "text-health"; // Green
    } else if (bmi < 30) {
        category = window.toolsConfig.bmiOverweight || "Surpoids";
        colorClass = "text-yellow-500";
    } else {
        category = window.toolsConfig.bmiObese || "Obésité";
        colorClass = "text-accent"; // Red
    }

    if(bmiCategoryElement) {
        bmiCategoryElement.innerText = category;
        bmiCategoryElement.className = `block text-sm font-bold mt-1 font-mono uppercase tracking-wider ${colorClass}`;
    }
    
    if(resultContainer) resultContainer.classList.remove('hidden');
}

/* --- Macros / Metabolic Profile --- */
function calculateMacros() {
    const weight = parseFloat(document.getElementById('macro-weight').value);
    const height = parseFloat(document.getElementById('macro-height').value);
    const age = parseFloat(document.getElementById('macro-age').value);
    const gender = document.getElementById('macro-gender').value;
    const activity = parseFloat(document.getElementById('macro-activity').value);

    if (!weight || !height || !age || !gender || !activity) {
        alert(window.toolsConfig.alertMissingData || "Veuillez remplir tous les champs.");
        return;
    }

    // Mifflin-St Jeor Equation
    let bmr = (10 * weight) + (6.25 * height) - (5 * age);
    if (gender === 'male') {
        bmr += 5;
    } else {
        bmr -= 161;
    }

    const tdee = bmr * activity;

    const bmrElement = document.getElementById('bmr-value');
    const tdeeElement = document.getElementById('tdee-value');

    if(bmrElement) bmrElement.innerText = Math.round(bmr) + " kcal";
    if(tdeeElement) tdeeElement.innerText = Math.round(tdee) + " kcal";
}

/* --- Stopwatch Logic --- */
let stopwatchInterval;
let stopwatchTime = 0;
let stopwatchRunning = false;

function startStopwatch() {
    const btn = document.getElementById('btn-start-stopwatch');
    if (!stopwatchRunning) {
        stopwatchRunning = true;
        if(btn) btn.innerText = window.toolsConfig.btnPause || "Pause";
        const startTime = Date.now() - stopwatchTime;
        stopwatchInterval = setInterval(() => {
            stopwatchTime = Date.now() - startTime;
            updateStopwatchDisplay();
        }, 10);
    } else {
        stopwatchRunning = false;
        if(btn) btn.innerText = window.toolsConfig.btnResume || "Reprendre";
        clearInterval(stopwatchInterval);
    }
}

function resetStopwatch() {
    stopwatchRunning = false;
    clearInterval(stopwatchInterval);
    stopwatchTime = 0;
    updateStopwatchDisplay();
    const btn = document.getElementById('btn-start-stopwatch');
    if(btn) btn.innerText = window.toolsConfig.btnStart || "Démarrer";
}

function updateStopwatchDisplay() {
    const time = new Date(stopwatchTime);
    const minutes = String(time.getUTCMinutes()).padStart(2, '0');
    const seconds = String(time.getUTCSeconds()).padStart(2, '0');
    const milliseconds = String(Math.floor(time.getUTCMilliseconds() / 10)).padStart(2, '0');
    const display = document.getElementById('stopwatch-display');
    if(display) display.innerText = `${minutes}:${seconds}.${milliseconds}`;
}

/* --- Timer Logic --- */
let timerInterval;
let timerTime = 0;
let timerRunning = false;

function startTimer() {
    const btn = document.getElementById('btn-start-timer');
    const display = document.getElementById('timer-display');
    const inputs = document.querySelectorAll('#timer-ui input');
    const separator = document.querySelector('#timer-ui span');

    if (!timerRunning) {
        if (timerTime === 0) {
            const min = parseInt(document.getElementById('timer-min').value) || 0;
            const sec = parseInt(document.getElementById('timer-sec').value) || 0;
            timerTime = (min * 60 + sec) * 1000;
        }

        if (timerTime > 0) {
            timerRunning = true;
            if(btn) btn.innerText = window.toolsConfig.btnPause || "Pause";
            inputs.forEach(i => i.classList.add('hidden'));
            if(separator) separator.classList.add('hidden');
            if(display) display.classList.remove('hidden');
            updateTimerDisplay();

            const endTime = Date.now() + timerTime;
            
            timerInterval = setInterval(() => {
                const remaining = endTime - Date.now();
                if (remaining <= 0) {
                    clearInterval(timerInterval);
                    timerTime = 0;
                    timerRunning = false;
                    if(display) display.innerText = "00:00";
                    if(btn) btn.innerText = window.toolsConfig.btnStart || "Démarrer";
                    alert(window.toolsConfig.alertTimeUp || "Temps écoulé !");
                    resetTimer(); // Reset UI
                } else {
                    timerTime = remaining;
                    updateTimerDisplay();
                }
            }, 100);
        }
    } else {
        timerRunning = false;
        if(btn) btn.innerText = window.toolsConfig.btnResume || "Reprendre";
        clearInterval(timerInterval);
    }
}

function resetTimer() {
    timerRunning = false;
    clearInterval(timerInterval);
    timerTime = 0;
    
    const btn = document.getElementById('btn-start-timer');
    if(btn) btn.innerText = window.toolsConfig.btnStart || "Démarrer";
    
    const display = document.getElementById('timer-display');
    if(display) display.classList.add('hidden');
    
    document.querySelectorAll('#timer-ui input').forEach(i => i.classList.remove('hidden'));
    const separator = document.querySelector('#timer-ui span');
    if(separator) separator.classList.remove('hidden');
    
    document.getElementById('timer-min').value = '00';
    document.getElementById('timer-sec').value = '00';
}

function updateTimerDisplay() {
    const totalSeconds = Math.ceil(timerTime / 1000);
    const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, '0');
    const seconds = String(totalSeconds % 60).padStart(2, '0');
    const display = document.getElementById('timer-display');
    if(display) display.innerText = `${minutes}:${seconds}`;
}

/* --- Tab Switching --- */
function switchTab(tab) {
    const stopwatchUI = document.getElementById('stopwatch-ui');
    const timerUI = document.getElementById('timer-ui');
    const tabStopwatch = document.getElementById('tab-stopwatch');
    const tabTimer = document.getElementById('tab-timer');

    if(tab === 'stopwatch') {
        if(stopwatchUI) stopwatchUI.classList.remove('hidden');
        if(timerUI) timerUI.classList.add('hidden');
        
        if(tabStopwatch) {
            tabStopwatch.classList.add('text-health', 'border-b-2', 'border-health');
            tabStopwatch.classList.remove('text-gray-500');
        }
        
        if(tabTimer) {
            tabTimer.classList.remove('text-health', 'border-b-2', 'border-health');
            tabTimer.classList.add('text-gray-500');
        }
    } else {
        if(stopwatchUI) stopwatchUI.classList.add('hidden');
        if(timerUI) timerUI.classList.remove('hidden');
        
        if(tabTimer) {
            tabTimer.classList.add('text-health', 'border-b-2', 'border-health');
            tabTimer.classList.remove('text-gray-500');
        }
        
        if(tabStopwatch) {
            tabStopwatch.classList.remove('text-health', 'border-b-2', 'border-health');
            tabStopwatch.classList.add('text-gray-500');
        }
    }
}
