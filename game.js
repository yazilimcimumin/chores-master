// Game state
let currentGame = null;
let gameState = {};

// Sound functions
function playSound(soundId) {
    const sound = document.getElementById(soundId);
    if (sound) {
        sound.currentTime = 0;
        sound.play().catch(e => console.log('Sound play failed:', e));
    }
}

// Utility functions
function shuffle(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

function getRandomPairs(count) {
    return shuffle(WORD_PAIRS).slice(0, count);
}

function formatMoney(amount) {
    return `₺${amount.toLocaleString('tr-TR')}`;
}

// Screen management
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
}

function backToMenu() {
    currentGame = null;
    gameState = {};
    showScreen('menu-screen');
}

// Start game
function startGame(mode) {
    playSound('thinking-sound');
    currentGame = mode;
    
    switch(mode) {
        case 'quiz':
            startQuizGame();
            break;
        case 'speed':
            startSpeedGame();
            break;
        case 'match':
            startMatchGame();
            break;
        case 'timed':
            startTimedGame();
            break;
    }
}

// ===== QUIZ GAME =====
function startQuizGame() {
    showScreen('quiz-screen');
    gameState = {
        questionNum: 0,
        score: 0,
        usedPairs: [],
        gameOver: false
    };
    nextQuizQuestion();
}

function nextQuizQuestion() {
    if (gameState.questionNum >= 15 || gameState.gameOver) {
        showQuizGameOver();
        return;
    }
    
    const availablePairs = WORD_PAIRS.filter(p => !gameState.usedPairs.includes(p));
    const pair = availablePairs[Math.floor(Math.random() * availablePairs.length)];
    gameState.usedPairs.push(pair);
    
    const isEnglishQuestion = Math.random() > 0.5;
    const question = isEnglishQuestion ? pair[0] : pair[1];
    const correctAnswer = isEnglishQuestion ? pair[1] : pair[0];
    
    const wrongAnswers = shuffle(
        WORD_PAIRS
            .filter(p => p !== pair)
            .map(p => isEnglishQuestion ? p[1] : p[0])
    ).slice(0, 3);
    
    const options = shuffle([correctAnswer, ...wrongAnswers]);
    
    gameState.currentQuestion = { question, correctAnswer, options };
    
    document.getElementById('quiz-question-num').textContent = `Soru ${gameState.questionNum + 1}/15`;
    document.getElementById('quiz-score').textContent = `Kazanılan: ${formatMoney(gameState.score)}`;
    document.getElementById('quiz-prize').textContent = `Ödül: ${formatMoney(PRIZE_LADDER[gameState.questionNum])}`;
    document.getElementById('quiz-question').textContent = question;
    document.getElementById('quiz-feedback').textContent = '';
    
    const optionsContainer = document.getElementById('quiz-options');
    optionsContainer.innerHTML = '';
    
    const colors = ['#3498db', '#2ecc71', '#e67e22', '#9b59b6'];
    const labels = ['A:', 'B:', 'C:', 'D:'];
    
    options.forEach((option, i) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.style.background = colors[i];
        btn.textContent = `${labels[i]} ${option}`;
        btn.onclick = () => checkQuizAnswer(option, btn);
        optionsContainer.appendChild(btn);
    });
}

function checkQuizAnswer(answer, btn) {
    const buttons = document.querySelectorAll('#quiz-options .option-btn');
    buttons.forEach(b => b.classList.add('disabled'));
    
    const feedback = document.getElementById('quiz-feedback');
    
    if (answer === gameState.currentQuestion.correctAnswer) {
        btn.classList.add('correct');
        playSound('correct-sound');
        gameState.score = PRIZE_LADDER[gameState.questionNum];
        gameState.questionNum++;
        feedback.textContent = 'DOĞRU!';
        feedback.className = 'feedback correct';
        
        setTimeout(() => {
            if (gameState.questionNum < 15) {
                nextQuizQuestion();
            } else {
                showQuizGameOver();
            }
        }, 2000);
    } else {
        btn.classList.add('wrong');
        playSound('wrong-sound');
        gameState.gameOver = true;
        feedback.textContent = `YANLIŞ! Doğru cevap: ${gameState.currentQuestion.correctAnswer}`;
        feedback.className = 'feedback wrong';
        
        setTimeout(showQuizGameOver, 3000);
    }
}

function showQuizGameOver() {
    const container = document.getElementById('quiz-options');
    const message = gameState.questionNum >= 15 ? 
        '<h2 style="color: #ffc300;">TEBRİKLER! MİLYONER OLDUNUZ!</h2>' :
        '<h2 style="color: #e74c3c;">OYUN BİTTİ!</h2>';
    
    container.innerHTML = `
        <div class="game-over">
            ${message}
            <p>Kazandığınız Para: ${formatMoney(gameState.score)}</p>
            <button class="submit-btn" onclick="backToMenu()">Ana Menüye Dön</button>
        </div>
    `;
    document.getElementById('quiz-question').textContent = '';
    document.getElementById('quiz-feedback').textContent = '';
}

// ===== SPEED GAME =====
function startSpeedGame() {
    showScreen('speed-screen');
    gameState = {
        score: 0,
        answered: 0,
        timeLeft: 30,
        usedPairs: []
    };
    
    nextSpeedQuestion();
    startSpeedTimer();
}

function startSpeedTimer() {
    gameState.timerInterval = setInterval(() => {
        gameState.timeLeft--;
        const timerEl = document.getElementById('speed-timer');
        timerEl.textContent = `${gameState.timeLeft}s`;
        
        if (gameState.timeLeft < 10) {
            timerEl.classList.add('warning');
        }
        
        if (gameState.timeLeft <= 0) {
            clearInterval(gameState.timerInterval);
            showSpeedGameOver();
        }
    }, 1000);
}

function nextSpeedQuestion() {
    const availablePairs = WORD_PAIRS.filter(p => !gameState.usedPairs.includes(p));
    if (availablePairs.length === 0) {
        gameState.usedPairs = [];
    }
    
    const pair = availablePairs[Math.floor(Math.random() * (availablePairs.length || WORD_PAIRS.length))];
    gameState.usedPairs.push(pair);
    
    const isEnglishQuestion = Math.random() > 0.5;
    gameState.currentQuestion = isEnglishQuestion ? pair[0] : pair[1];
    gameState.correctAnswer = isEnglishQuestion ? pair[1] : pair[0];
    
    document.getElementById('speed-question').textContent = gameState.currentQuestion;
    document.getElementById('speed-input').value = '';
    document.getElementById('speed-input').focus();
    document.getElementById('speed-feedback').textContent = '';
}

function checkSpeedAnswer() {
    if (gameState.timeLeft <= 0) return;
    
    const input = document.getElementById('speed-input').value.trim().toLowerCase();
    const correct = gameState.correctAnswer.toLowerCase();
    const feedback = document.getElementById('speed-feedback');
    
    if (input === correct) {
        playSound('correct-sound');
        gameState.score += 10;
        gameState.answered++;
        feedback.textContent = 'DOĞRU! +10 puan';
        feedback.className = 'feedback correct';
    } else {
        playSound('wrong-sound');
        feedback.textContent = `YANLIŞ! Doğru: ${gameState.correctAnswer}`;
        feedback.className = 'feedback wrong';
    }
    
    document.getElementById('speed-score').textContent = `Puan: ${gameState.score}`;
    document.getElementById('speed-answered').textContent = `Cevaplanan: ${gameState.answered}`;
    
    setTimeout(() => {
        if (gameState.timeLeft > 0) {
            nextSpeedQuestion();
        }
    }, 1000);
}

document.getElementById('speed-input')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        checkSpeedAnswer();
    }
});

function showSpeedGameOver() {
    document.getElementById('speed-question').innerHTML = `
        <div class="game-over">
            <h2 style="color: #e74c3c;">SÜRE BİTTİ!</h2>
            <p>Toplam Puan: ${gameState.score}</p>
            <p>Cevaplanan Soru: ${gameState.answered}</p>
            <button class="submit-btn" onclick="backToMenu()">Ana Menüye Dön</button>
        </div>
    `;
    document.getElementById('speed-input').style.display = 'none';
    document.getElementById('speed-submit').style.display = 'none';
    document.getElementById('speed-feedback').textContent = '';
}

// ===== MATCH GAME =====
function startMatchGame() {
    showScreen('match-screen');
    
    const pairs = getRandomPairs(8);
    const englishWords = pairs.map(p => p[0]);
    const turkishWords = shuffle(pairs.map(p => p[1]));
    
    gameState = {
        score: 0,
        pairs: pairs,
        selectedEnglish: null,
        selectedTurkish: null,
        matched: []
    };
    
    const englishContainer = document.getElementById('english-words');
    const turkishContainer = document.getElementById('turkish-words');
    
    englishContainer.innerHTML = '';
    turkishContainer.innerHTML = '';
    
    englishWords.forEach((word, i) => {
        const btn = document.createElement('button');
        btn.className = 'word-btn english-word';
        btn.textContent = word;
        btn.dataset.word = word;
        btn.onclick = () => selectEnglishWord(btn);
        englishContainer.appendChild(btn);
    });
    
    turkishWords.forEach((word, i) => {
        const btn = document.createElement('button');
        btn.className = 'word-btn turkish-word';
        btn.textContent = word;
        btn.dataset.word = word;
        btn.onclick = () => selectTurkishWord(btn);
        turkishContainer.appendChild(btn);
    });
    
    document.getElementById('match-score').textContent = `Puan: 0`;
    document.getElementById('match-feedback').textContent = '';
}

function selectEnglishWord(btn) {
    if (btn.classList.contains('matched')) return;
    
    document.querySelectorAll('.english-word').forEach(b => b.classList.remove('selected'));
    
    if (gameState.selectedEnglish === btn) {
        gameState.selectedEnglish = null;
    } else {
        btn.classList.add('selected');
        gameState.selectedEnglish = btn;
        playSound('thinking-sound');
    }
}

function selectTurkishWord(btn) {
    if (btn.classList.contains('matched')) return;
    
    document.querySelectorAll('.turkish-word').forEach(b => b.classList.remove('selected'));
    
    if (gameState.selectedTurkish === btn) {
        gameState.selectedTurkish = null;
    } else {
        btn.classList.add('selected');
        gameState.selectedTurkish = btn;
        playSound('thinking-sound');
        
        if (gameState.selectedEnglish && gameState.selectedTurkish) {
            checkMatch();
        }
    }
}

function checkMatch() {
    const engWord = gameState.selectedEnglish.dataset.word;
    const turWord = gameState.selectedTurkish.dataset.word;
    
    const isCorrect = gameState.pairs.some(p => p[0] === engWord && p[1] === turWord);
    
    const feedback = document.getElementById('match-feedback');
    
    if (isCorrect) {
        playSound('correct-sound');
        gameState.selectedEnglish.classList.add('matched');
        gameState.selectedTurkish.classList.add('matched');
        gameState.score += 10;
        gameState.matched.push([engWord, turWord]);
        feedback.textContent = 'MÜKEMMEL!';
        feedback.className = 'feedback correct';
        
        document.getElementById('match-score').textContent = `Puan: ${gameState.score}`;
        
        if (gameState.matched.length === 8) {
            setTimeout(showMatchGameOver, 1000);
        }
    } else {
        playSound('wrong-sound');
        feedback.textContent = 'TEKRAR DENE!';
        feedback.className = 'feedback wrong';
    }
    
    gameState.selectedEnglish.classList.remove('selected');
    gameState.selectedTurkish.classList.remove('selected');
    gameState.selectedEnglish = null;
    gameState.selectedTurkish = null;
    
    setTimeout(() => {
        feedback.textContent = '';
    }, 1000);
}

function showMatchGameOver() {
    document.getElementById('english-words').innerHTML = `
        <div class="game-over" style="grid-column: 1 / -1;">
            <h2 style="color: #ffc300;">TEBRİKLER!</h2>
            <p>Toplam Puan: ${gameState.score}</p>
            <button class="submit-btn" onclick="backToMenu()">Ana Menüye Dön</button>
        </div>
    `;
    document.getElementById('turkish-words').innerHTML = '';
    document.getElementById('match-feedback').textContent = '';
}

// ===== TIMED GAME =====
function startTimedGame() {
    showScreen('timed-screen');
    gameState = {
        score: 0,
        found: 0,
        total: 10,
        timeLeft: 60,
        usedPairs: []
    };
    
    nextTimedQuestion();
    startTimedTimer();
}

function startTimedTimer() {
    gameState.timerInterval = setInterval(() => {
        gameState.timeLeft--;
        const timerEl = document.getElementById('timed-timer');
        timerEl.textContent = `${gameState.timeLeft}s`;
        
        if (gameState.timeLeft < 15) {
            timerEl.classList.add('warning');
        }
        
        if (gameState.timeLeft <= 0) {
            clearInterval(gameState.timerInterval);
            showTimedGameOver();
        }
    }, 1000);
}

function nextTimedQuestion() {
    if (gameState.found >= gameState.total) {
        clearInterval(gameState.timerInterval);
        showTimedGameOver();
        return;
    }
    
    const availablePairs = WORD_PAIRS.filter(p => !gameState.usedPairs.includes(p));
    const pair = availablePairs[Math.floor(Math.random() * availablePairs.length)];
    gameState.usedPairs.push(pair);
    
    const isEnglishQuestion = Math.random() > 0.5;
    const question = isEnglishQuestion ? pair[0] : pair[1];
    const correctAnswer = isEnglishQuestion ? pair[1] : pair[0];
    
    const wrongAnswers = shuffle(
        WORD_PAIRS
            .filter(p => p !== pair)
            .map(p => isEnglishQuestion ? p[1] : p[0])
    ).slice(0, 3);
    
    const options = shuffle([correctAnswer, ...wrongAnswers]);
    
    gameState.currentQuestion = { question, correctAnswer, options };
    
    document.getElementById('timed-progress').textContent = `İlerleme: ${gameState.found}/${gameState.total}`;
    document.getElementById('timed-score').textContent = `Puan: ${gameState.score}`;
    document.getElementById('timed-question').textContent = question;
    document.getElementById('timed-feedback').textContent = '';
    
    const optionsContainer = document.getElementById('timed-options');
    optionsContainer.innerHTML = '';
    
    const colors = ['#3498db', '#2ecc71', '#e67e22', '#9b59b6'];
    
    options.forEach((option, i) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.style.background = colors[i];
        btn.textContent = option;
        btn.onclick = () => checkTimedAnswer(option, btn);
        optionsContainer.appendChild(btn);
    });
}

function checkTimedAnswer(answer, btn) {
    if (gameState.timeLeft <= 0) return;
    
    const buttons = document.querySelectorAll('#timed-options .option-btn');
    buttons.forEach(b => b.classList.add('disabled'));
    
    const feedback = document.getElementById('timed-feedback');
    
    if (answer === gameState.currentQuestion.correctAnswer) {
        btn.classList.add('correct');
        playSound('correct-sound');
        gameState.score += 10;
        gameState.found++;
        feedback.textContent = `DOĞRU! ${gameState.found}/${gameState.total}`;
        feedback.className = 'feedback correct';
    } else {
        btn.classList.add('wrong');
        playSound('wrong-sound');
        feedback.textContent = 'YANLIŞ!';
        feedback.className = 'feedback wrong';
    }
    
    setTimeout(() => {
        if (gameState.timeLeft > 0 && gameState.found < gameState.total) {
            nextTimedQuestion();
        } else if (gameState.found >= gameState.total) {
            clearInterval(gameState.timerInterval);
            showTimedGameOver();
        }
    }, 800);
}

function showTimedGameOver() {
    const container = document.getElementById('timed-options');
    const message = gameState.found >= gameState.total ?
        '<h2 style="color: #ffc300;">TEBRİKLER! KAZANDIN!</h2>' :
        '<h2 style="color: #e74c3c;">SÜRE BİTTİ!</h2>';
    
    container.innerHTML = `
        <div class="game-over">
            ${message}
            <p>Toplam Puan: ${gameState.score}</p>
            <p>Bulunan Kelime: ${gameState.found}/${gameState.total}</p>
            <button class="submit-btn" onclick="backToMenu()">Ana Menüye Dön</button>
        </div>
    `;
    document.getElementById('timed-question').textContent = '';
    document.getElementById('timed-feedback').textContent = '';
}
