/**
 * QuizMaster - Interactive Frontend Script
 * Is file mein option selection highlighting, timer aur form submit confirmation ka code hai.
 */

// Jab poora HTML DOM load ho jaye tab yeh code execute hoga
document.addEventListener('DOMContentLoaded', () => {

    // =============================================================
    // 1. RADIO OPTION SELECTION INTERACTION
    // =============================================================
    // Page par maujood saare option labels ko select kar rahe hain
    const optionLabels = document.querySelectorAll('.option-label');

    // Har option label par loop chala rahe hain
    optionLabels.forEach(label => {
        // Label ke andar wale radio input button ko dhoondh rahe hain
        const radio = label.querySelector('.option-radio');
        
        // Agar radio input milta hai
        if (radio) {
            // Radio button change hone par event listener lagaya
            radio.addEventListener('change', () => {
                // Us sawal ka parent options group container dhoondh rahe hain
                const parentGroup = label.closest('.options-group');
                
                // Agar parent group milta hai
                if (parentGroup) {
                    // Us sawal ke baaki saare sibling options se 'selected-option' class hata do
                    parentGroup.querySelectorAll('.option-label').forEach(sibling => {
                        sibling.classList.remove('selected-option');
                    });
                }
                
                // Agar yeh radio button select (checked) hua hai
                if (radio.checked) {
                    // Is label ko highlight karne ke liye 'selected-option' class jod do
                    label.classList.add('selected-option');
                }

                // Agar is question par pehle 'unanswered' ka warning border tha, toh use hata do
                const questionCard = label.closest('.question-card');
                if (questionCard) {
                    questionCard.classList.remove('highlight-unanswered');
                }
            });
        }
    });


    // =============================================================
    // 2. QUIZ TIMER (STOPWATCH)
    // =============================================================
    // Header mein timer text dikhane wala HTML element pakad rahe hain
    const timerElement = document.getElementById('quizTimer');

    // Agar page par timer element maujood hai
    if (timerElement) {
        // Total seconds ka counter variable 0 se shuru karte hain
        let totalSeconds = 0;

        // Har second timer ko badhane aur format karne wala function
        const updateTimer = () => {
            // 1 second badhao
            totalSeconds++;
            
            // Minutes calculate karo (seconds divided by 60)
            const minutes = Math.floor(totalSeconds / 60);
            
            // Baki bache seconds calculate karo (seconds modulo 60)
            const seconds = totalSeconds % 60;

            // Single digit hone par aage '0' lagane ke liye padStart use kar rahe hain (e.g. 05)
            const formattedMinutes = String(minutes).padStart(2, '0');
            const formattedSeconds = String(seconds).padStart(2, '0');

            // Timer element ke text ko "MM:SS" format mein update karo
            timerElement.textContent = `${formattedMinutes}:${formattedSeconds}`;
        };

        // Har 1000 millisecond (1 second) mein updateTimer function ko call karo
        const timerInterval = setInterval(updateTimer, 1000);

        // Agar user page chhod kar kahin aur chala jaye toh timer band kar do
        window.addEventListener('beforeunload', () => {
            clearInterval(timerInterval);
        });
    }


    // =============================================================
    // 3. FORM SUBMISSION VALIDATION & CONFIRMATION
    // =============================================================
    // Quiz submit form ko get kar rahe hain
    const quizForm = document.getElementById('quizForm');

    // Agar quiz form page par maujood hai
    if (quizForm) {
        // Submit button dabane par event listener lagaya
        quizForm.addEventListener('submit', (e) => {
            // Saare questions cards ko select kar rahe hain
            const questionCards = document.querySelectorAll('.question-card');
            
            // Chhute huye (unanswered) questions ka counter
            let unansweredCount = 0;
            
            // Pehla chhuta hua sawal track karne ke liye variable (scroll karne ke liye)
            let firstUnansweredCard = null;

            // Har question card ko check karte hain
            questionCards.forEach(card => {
                // Card se question ID nikaalte hain
                const questionId = card.getAttribute('data-question-id');
                
                // Check karte hain ki kya is question ka koi radio button checked hai
                const checkedRadio = card.querySelector(`input[name="question_${questionId}"]:checked`);

                // Agar koi option select nahi hai
                if (!checkedRadio) {
                    // Unanswered count 1 se badhao
                    unansweredCount++;
                    
                    // Card par warning highlight class lagao
                    card.classList.add('highlight-unanswered');
                    
                    // Agar yeh pehla unanswered card hai toh ise save kar lo
                    if (!firstUnansweredCard) {
                        firstUnansweredCard = card;
                    }
                } else {
                    // Agar answered hai toh warning class hata do
                    card.classList.remove('highlight-unanswered');
                }
            });

            // Agar koi question chhuta hua hai
            if (unansweredCount > 0) {
                // Confirmation popup message banate hain
                const confirmMsg = `You have left ${unansweredCount} question(s) unanswered.\n\nAre you sure you want to submit anyway?`;
                
                // Agar user 'Cancel' dabata hai
                if (!confirm(confirmMsg)) {
                    // Form submission ko rok do (Cancel)
                    e.preventDefault();
                    
                    // Screen ko smooth scroll karke pehle chhute huye sawal par le jao
                    if (firstUnansweredCard) {
                        firstUnansweredCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return false;
                }
            } else {
                // Agar saare sawal attempt kiye hain toh normal confirmation pucho
                const confirmMsg = "Are you sure you want to submit your quiz?";
                
                // Agar user Cancel kare toh submission rok do
                if (!confirm(confirmMsg)) {
                    e.preventDefault();
                    return false;
                }
            }
        });
    }
});
