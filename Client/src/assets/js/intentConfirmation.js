import { validatedAction } from './dashboard.js';

export function confirmIntent(response, entities, flagWelcome) {
    console.log('Welcome flag: ', flagWelcome);
    const data = response;
    const message = data.response;
    const predictedLabel = data.predicted_label;
    const responseData = data.response_data;

    let hebrewResponseData = '';
    if (predictedLabel == 0) {
        hebrewResponseData = 'אני רוצה להזמין כרטיס';
    } else if (predictedLabel == 1) {
        hebrewResponseData = 'אני רוצה החזר על הכרטיס';
    } else if (predictedLabel == 2) {
        let intentVerifiedMessage = document.getElementById('chat-messages');
        let newIntentVerifiedMessage = document.createElement('div');
        newIntentVerifiedMessage.className = 'message-back';
        let messageText =
            'אני חושש שאני לא יודע לעזור לך בבקשה זו, אנא בקש שוב';
        if (flagWelcome) {
            messageText = 'שלום לך! ' + messageText;
        }
        newIntentVerifiedMessage.textContent = messageText;
        intentVerifiedMessage.appendChild(newIntentVerifiedMessage);
        intentVerifiedMessage.scrollTop = intentVerifiedMessage.scrollHeight;
        return;
    }

    let intentVerifiedMessage = document.getElementById('chat-messages');
    let newIntentVerifiedMessage = document.createElement('div');
    newIntentVerifiedMessage.className = 'message-back';
    let messageText =
        'זיהיתי את ההודעה שלך כ' + hebrewResponseData + ', האם זו כוונתך?';

    if (flagWelcome) {
        messageText = 'שלום לך! ' + messageText;
    }
    newIntentVerifiedMessage.textContent = messageText;
    intentVerifiedMessage.appendChild(newIntentVerifiedMessage);
    intentVerifiedMessage.scrollTop = intentVerifiedMessage.scrollHeight;

    let intentVerifiedRightMessage = document.getElementById('chat-messages');
    let newIntentVerifiedRightMessage = document.createElement('button');
    newIntentVerifiedRightMessage.className = 'message-back';
    newIntentVerifiedRightMessage.textContent = 'כן, זוהי כוונתי';
    newIntentVerifiedRightMessage.style.backgroundColor = 'green';
    newIntentVerifiedRightMessage.onclick = function () {
        const userConfirmed = true;
        console.log(userConfirmed);
        newIntentVerifiedRightMessage.disabled = true;
        newIntentVerifiedWrongMessage.disabled = true;
        confirmEntities(predictedLabel, entities);
    };
    intentVerifiedRightMessage.appendChild(newIntentVerifiedRightMessage);
    intentVerifiedRightMessage.scrollTop =
        intentVerifiedRightMessage.scrollHeight;

    let intentVerifiedWrongMessage = document.getElementById('chat-messages');
    let newIntentVerifiedWrongMessage = document.createElement('button');
    newIntentVerifiedWrongMessage.className = 'message-back';
    newIntentVerifiedWrongMessage.textContent = 'לא, זוהי לא כוונתי';
    newIntentVerifiedWrongMessage.style.backgroundColor = 'red';
    newIntentVerifiedWrongMessage.onclick = function () {
        const userConfirmed = false;
        console.log(userConfirmed);
        newIntentVerifiedRightMessage.disabled = true;
        newIntentVerifiedWrongMessage.disabled = true;
        wrongLabel();
    };
    intentVerifiedWrongMessage.appendChild(newIntentVerifiedWrongMessage);
    intentVerifiedWrongMessage.scrollTop =
        intentVerifiedWrongMessage.scrollHeight;


    function wrongLabel() {
        let intentVerifiedMessage = document.getElementById('chat-messages');

        if (intentVerifiedMessage) {
            let newIntentVerifiedMessage = document.createElement('div');
            newIntentVerifiedMessage.className = 'message-back';

            let messageText = 'איזה באסה שלא הצלחתי להבין את כוונתך, בוא ננסה שוב :';
            newIntentVerifiedMessage.textContent = messageText;

            intentVerifiedMessage.appendChild(newIntentVerifiedMessage);

            intentVerifiedMessage.scrollTop = intentVerifiedMessage.scrollHeight;
        } else {
            console.error("Chat messages container element not found.");
        }

        const options = ['הזמנת טיסה', 'ביטול טיסה'];
        const selectElement = document.createElement('select');
        selectElement.style.width = '150px';
        selectElement.style.marginRight = '10px';

        options.forEach(optionText => {
            const optionElement = document.createElement('option');
            optionElement.value = optionText.toLowerCase().replace(' ', '-');
            optionElement.textContent = optionText;
            selectElement.appendChild(optionElement);
        });

        const nextButton = document.createElement('button');
        nextButton.textContent = 'הבא';
        nextButton.style.padding = '5px 10px';
        nextButton.onclick = function() {
            const selectedValue = selectElement.value;
            if (selectedValue === 'הזמנת-טיסה') {
                nextButton.disabled = true;
                confirmEntities(0, entities);
            } else if (selectedValue === 'ביטול-טיסה') {
                nextButton.disabled = true;
                confirmEntities(1, entities);
            } else {
                nextButton.disabled = true;
                console.log("Unknown option selected");
            }
        };

        let dropdownContainer = document.getElementById('dropdown-container');

        // If dropdown container doesn't exist, create it
        if (!dropdownContainer) {
            dropdownContainer = document.createElement('div');
            dropdownContainer.id = 'dropdown-container';
            dropdownContainer.style.display = 'flex';
            dropdownContainer.style.justifyContent = 'flex-start';
            dropdownContainer.style.marginTop = '10px';

            intentVerifiedMessage.appendChild(dropdownContainer);
        }

        dropdownContainer.appendChild(selectElement);
        dropdownContainer.appendChild(nextButton);
    }

    /// Entities Confirmation :
    function confirmEntities(predictedLabel, entities) {
        const dictEntities = JSON.parse(entities);
        const requireEntities = [0, 0, 0, 0];
        if (predictedLabel == 0 || predictedLabel == 1) {
            requireEntities[0] = 1;
            requireEntities[1] = 1;
            requireEntities[2] = 1;
            requireEntities[3] = 0;
        }
        const existsEntities = [0, 0, 0, 0];
        if (dictEntities['Origin'] != null) existsEntities[0] = 1;
        if (dictEntities['Destination'] != null) existsEntities[1] = 1;
        if (dictEntities['Date'] != null) existsEntities[2] = 1;
        if (dictEntities['Date2'] != null) existsEntities[3] = 1;

        if (existsEntities[0] - requireEntities[0] < 0) return;
        //Missing Origin;
        if (existsEntities[1] - requireEntities[1] < 0) return;
        //Missing Destination;
        if (existsEntities[2] - requireEntities[2] < 0) return;
        //Missing Date;
        if (existsEntities[3] - requireEntities[3] < 0) return;
        //Missing Date2;

        validatedAction(predictedLabel, entities);
    }
}
