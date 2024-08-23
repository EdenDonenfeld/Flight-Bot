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
    };
    intentVerifiedWrongMessage.appendChild(newIntentVerifiedWrongMessage);
    intentVerifiedWrongMessage.scrollTop =
        intentVerifiedWrongMessage.scrollHeight;

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
