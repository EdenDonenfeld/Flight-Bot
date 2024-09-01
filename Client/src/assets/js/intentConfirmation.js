import { validatedAction } from './dashboard.js';

const APCode = {
    "ישראל": "TLV",
    "יוון": "ATH",
    "תל אביב": "TLV",
    "ניו יורק": "JFK",
    "לוס אנגלס": "LAX",
    "פריז": "CDG",
    "לונדון": "LHR",
    "ברלין": "TXL",
    "רומא": "FCO",
    "מדריד": "MAD",
    "אמסטרדם": "AMS",
    "פראג": "PRG",
    "בודפשט": "BUD",
    "וינה": "VIE",
    "פרנקפורט": "FRA",
    "מינכן": "MUC",
    "זיריך": "ZRH",
    "קופנהגן": "CPH",
    "אוסלו": "OSL",
    "סטוקהולם": "ARN",
    "הלסינקי": "HEL",
    "ריגה": "RIX",
    "וילנה": "VNO",
    "קייב": "KBP",
    "מוסקבה": "SVO",
    "סנט פטרסבורג": "LED",
    "קראקוב": "KRK",
    "וורשה": "WAW",
    "בוקרשט": "OTP",
    "סופיה": "SOF",
    "זלצבורג": "ZRH"
};

export function confirmIntent(response, entities, flagWelcome) {
    console.log('Welcome flag: ', flagWelcome);
    const data = response;
    const message = data.response;
    const predictedLabel = data.predicted_label;
    const responseData = data.response_data;

    let hebrewResponseData = '';
    if (predictedLabel == 0) {
        hebrewResponseData = 'אתה רוצה להזמין כרטיס';
    } else if (predictedLabel == 1) {
        hebrewResponseData = 'אתה רוצה החזר על הכרטיס';
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
    let messageText = 'לתחושתי ' + hebrewResponseData + ', האם זו כוונתך?';

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

            let messageText =
                'איזה באסה שלא הצלחתי להבין את כוונתך, בוא ננסה שוב :';
            newIntentVerifiedMessage.textContent = messageText;

            intentVerifiedMessage.appendChild(newIntentVerifiedMessage);

            intentVerifiedMessage.scrollTop =
                intentVerifiedMessage.scrollHeight;
        } else {
            console.error('Chat messages container element not found.');
        }

        const options = ['הזמנת טיסה', 'ביטול טיסה'];
        const selectElement = document.createElement('select');
        selectElement.style.width = '150px';
        selectElement.style.marginRight = '10px';

        options.forEach((optionText) => {
            const optionElement = document.createElement('option');
            optionElement.value = optionText.toLowerCase().replace(' ', '-');
            optionElement.textContent = optionText;
            selectElement.appendChild(optionElement);
        });

        const nextButton = document.createElement('button');
        nextButton.textContent = 'הבא';
        nextButton.style.padding = '5px 10px';
        nextButton.onclick = function () {
            const selectedValue = selectElement.value;
            if (selectedValue === 'הזמנת-טיסה') {
                nextButton.disabled = true;
                confirmEntities(0, entities);
            } else if (selectedValue === 'ביטול-טיסה') {
                nextButton.disabled = true;
                confirmEntities(1, entities);
            } else {
                nextButton.disabled = true;
                console.log('Unknown option selected');
            }
        };

        let dropdownContainer = document.getElementById('dropdown-container');

        // If dropdown container doesn't exist, create it
        if (!dropdownContainer) {
            dropdownContainer = document.createElement('div');
            dropdownContainer.id = 'dropdown-container';
            dropdownContainer.style.display = 'flex';
            dropdownContainer.style.justifyContent = 'flex-end';
            dropdownContainer.style.marginTop = '10px';
            dropdownContainer.style.marginBottom = '10px';

            intentVerifiedMessage.appendChild(dropdownContainer);
        }

        dropdownContainer.appendChild(selectElement);
        dropdownContainer.appendChild(nextButton);
    }

    /// Entities Confirmation :
    function confirmEntities(predictedLabel, entities) {
        const dictEntities = JSON.parse(entities);
        /*const requireEntities = [0, 0, 0, 0];
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
        if (dictEntities['Date2'] != null) existsEntities[3] = 1;*/

        if (dictEntities['Origin'] == false) {
            console.log('Missing Origin');
            return;
        } //Missing Origin - UnRealvent(Default TLV);
        if (dictEntities['Destination'] == false) {
            let requireDestinationMessage = document.getElementById('chat-messages');
            let newRequireDestinationMessage = document.createElement('div');
            newRequireDestinationMessage.className = 'message-back';
            newRequireDestinationMessage.textContent =
                'מתנצל, לא הצלחתי להבין מה היעד שאנחנו טסים אליו, בוא ננסה שוב. מה היעד אליו אנחנו טסים ?';
    
            // Create destination dropdown with autocomplete
            let destinationSelect = createAutocompleteDropdown();
            newRequireDestinationMessage.appendChild(destinationSelect);
    
            // Create "Next" button
            let nextButton = document.createElement('button');
            nextButton.textContent = 'הבא';
            nextButton.className = 'message-back next-button';
            newRequireDestinationMessage.appendChild(nextButton);
    
            // Append the message with the dropdown and button to the chat
            requireDestinationMessage.appendChild(newRequireDestinationMessage);
            requireDestinationMessage.scrollTop = requireDestinationMessage.scrollHeight;
    
            // Add event listener for the "Next" button
            nextButton.addEventListener('click', function () {
                let selectedDestination = destinationSelect.querySelector('input').value;
    
                if (selectedDestination) {
                    // Save the selected destination in dictEntities
                    dictEntities['Destination'] = selectedDestination;
    
                    const finalDestination = APCode[selectedDestination];
                    dictEntities['Destination'] = finalDestination;
                    entities = JSON.stringify(dictEntities);
                    lockContainer(destinationSelect);
                    validatedAction(predictedLabel, entities);
                } else {
                    // If no destination is selected, prompt the user
                    let errorMessage = document.createElement('div');
                    errorMessage.className = 'message-back';
                    errorMessage.textContent = 'אנא בחר יעד לפני שממשיך.';
                    requireDestinationMessage.appendChild(errorMessage);
                    requireDestinationMessage.scrollTop = requireDestinationMessage.scrollHeight;
                }
            });
    
            return;
        } //Missing Destination;
        if (dictEntities['Date'] == false) {
            let requireDestinationMessage =
                document.getElementById('chat-messages');
            let newRequireDestinationMessage = document.createElement('div');
            newRequireDestinationMessage.className = 'message-back';
            newRequireDestinationMessage.textContent =
                'מתנצל, לא הצלחתי להבין באיזה תאריך אנחנו טסים, בוא ננסה שוב. אנא הזן תאריך';
            requireDestinationMessage.appendChild(newRequireDestinationMessage);
            requireDestinationMessage.scrollTop =
                requireDestinationMessage.scrollHeight;

            let dateInput = document.createElement('input'); //Date Input
            dateInput.type = 'date';
            dateInput.className = 'date-selector';

            let nextButton = document.createElement('button'); //Next button
            nextButton.textContent = 'הבא';
            nextButton.className = 'message-back next-button';

            newRequireDestinationMessage.appendChild(dateInput);
            newRequireDestinationMessage.appendChild(nextButton);

            requireDestinationMessage.appendChild(newRequireDestinationMessage);
            requireDestinationMessage.scrollTop =
                requireDestinationMessage.scrollHeight;

            nextButton.addEventListener('click', function () {
                let selectedDate = dateInput.value;
                if (selectedDate) {
                    const [year, month, day] = selectedDate.split('-');
                    const finalDate = `${day}/${month}/${year}`;
                    dictEntities['Date'] = finalDate;
                    entities = JSON.stringify(dictEntities);
                    dateInput.disabled = true;
                    validatedAction(predictedLabel, entities);
                } else {
                    let errorMessage = document.createElement('div');
                    errorMessage.className = 'message-back';
                    errorMessage.textContent = 'אנא בחר תאריך לפני שממשיך.';
                    requireDestinationMessage.appendChild(errorMessage);
                    requireDestinationMessage.scrollTop =
                        requireDestinationMessage.scrollHeight;
                }
            });
            return;
        } //Missing Date;
        if (dictEntities['Date2'] == false) {
            console.log('Missing Date2');
            return;
        } //Missing Date2 - UnRealvent;

        // The createDestinationDropdown function from the previous step
        function createAutocompleteDropdown() {
            let container = document.createElement('div');
            container.className = 'autocomplete-container';
        
            let input = document.createElement('input');
            input.setAttribute('type', 'text');
            input.setAttribute('placeholder', 'הקלד יעד...');
        
            let dropdown = document.createElement('ul');
            dropdown.className = 'autocomplete-dropdown';
        
            input.addEventListener('input', function() {
                // Clear current dropdown options
                dropdown.innerHTML = '';
        
                let filter = input.value.toLowerCase();
                for (let destination in APCode) {
                    if (destination.toLowerCase().includes(filter)) {
                        let item = document.createElement('li');
                        item.textContent = destination;
                        item.dataset.value = APCode[destination];
                        item.addEventListener('click', function() {
                            input.value = destination;
                            dropdown.innerHTML = ''; // Clear dropdown after selection
                        });
                        dropdown.appendChild(item);
                    }
                }
        
                if (dropdown.childElementCount === 0) {
                    let noMatchItem = document.createElement('li');
                    noMatchItem.textContent = 'לא נמצאו תוצאות';
                    dropdown.appendChild(noMatchItem);
                }
            });
        
            container.appendChild(input);
            container.appendChild(dropdown);
        
            return container;
        }

        function lockContainer(container) {
            let input = container.querySelector('input');
            input.disabled = true; // Disable input
            let dropdown = container.querySelector('.autocomplete-dropdown');
            dropdown.style.display = 'none'; // Hide the dropdown
        }

        validatedAction(predictedLabel, entities);
    }
}
