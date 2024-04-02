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

import spawn from "child_process"

export function analyzeMessage(sentence) {
    return new Promise((resolve, reject) => {
        const child = spawn("python", ["nlpAnalyze.py", sentence]);
        child.stdout.on('data', (data) => {
          resolve(data.toString());
        })
        child.stderr.on('data', (data) => {
          reject(data.toString());
        })
      })
}



  