function confirmIntent(label) {
    let hebrewResponseData = "";
    if (responseData == "you want to order a ticket") {
        hebrewResponseData = "אני רוצה להזמין כרטיס";
    }
    else if (responseData == "you want to refund a ticket") {
        hebrewResponseData = "אני רוצה החזר על הכרטיס";
    }
    else if (responseData == "you want to check the status of your ticket") {
        hebrewResponseData = "אני רוצה לבדוק סטטוס של כרטיס";
    }
    else if (responseData == "you want to change the date of your ticket") {
        hebrewResponseData = "אני רוצה לשנות את התאריך של הכרטיס";
    }
    else if (responseData == "you want to change the destination of your ticket") {
        hebrewResponseData = "אני רוצה לשנות את היעד של הכרטיס";
    }
    else if (responseData == "you want to know the weather of your destination") {
        hebrewResponseData = "אני רוצה לדעת את המזג אוויר ביעד";
    }
    else if (responseData == "you want to know what is allowed in the flight") {
        hebrewResponseData = "אני רוצה לדעת מה מותר לעלות לטיסה";
    }

    let intentVerifiedMessage = document.getElementById('chat-messages');
    let newIntentVerifiedMessage = document.createElement('div');
    newIntentVerifiedMessage.className = 'message-back';
    newIntentVerifiedMessage.textContent =
        'זיהיתי את ההודעה שלך כ: ' + hebrewResponseData + ', האם זו כוונתך?';
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
        validatedAction(predictedLabel, entities);
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
    intentVerifiedWrongMessage.scrollTop = intentVerifiedWrongMessage.scrollHeight;

    // if (newIntentVerifiedWrongMessage.textContent = "לא, זוהי לא כוונתי") {
    // // הודעת נסח מחדש
    // }



    return label
}