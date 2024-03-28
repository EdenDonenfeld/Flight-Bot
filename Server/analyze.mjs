// export function analyzeMessage(message) {
//     let response = `הבוט החזיר : ${message}`;
//     return response;
//   }

import { BertForSequenceClassification, BertTokenizer } from '@xenova/transformers';

// Load tokenizer and model
async function loadModel(modelPath) {
    const tokenizer = await BertTokenizer.from_pretrained('bert-base-multilingual-cased');
    const model = await BertForSequenceClassification.from_pretrained(modelPath);
    return { tokenizer, model };
}

// Function to classify a sentence
async function classifySentence(tokenizer, model, sentence) {
    // Tokenize and encode the input sentence
    const inputs = await tokenizer.encode(sentence, { padding: 'max_length', truncation: true, returnTensor: true });

    // Make prediction
    const logits = await model.predict(inputs);

    // Get predicted class label
    const predictedClass = await logits.argMax().data();
    return predictedClass[0];
}

// Example usage
async function analyzeMessage() {
    const modelPath = './saved_model';  // Path to the directory where you saved your trained model
    const { tokenizer, model } = await loadModel(modelPath);

    const sentence = "אני רוצה לשנות את הזמן של הטיסה שלי";
    const predictedLabel = await classifySentence(tokenizer, model, sentence);
    console.log("Predicted Label:", predictedLabel);
}

analyzeMessage();


  