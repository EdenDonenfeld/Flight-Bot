import express from "express";
import cors from "cors";
import {analyzeMessage} from "./analyze.mjs";
import path from "path";

const __dirname = path.resolve();

const app = express();
const port = 3000;
app.use(cors());

app.use(express.static(path.join(__dirname, '..','Client')));
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '..','Client','index.html'));
})

app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, '..','Client','src', 'pages', 'dashboard.html'));
})

app.get('/signUp', (req, res) => {
  res.sendFile(path.join(__dirname, '..','Client','src', 'pages', 'signUp.html'));
})

app.get('/seatOrder', (req, res) => {
  res.sendFile(path.join(__dirname, '..','Client','src', 'pages', 'seatOrder.html'));
})

app.get('/myTickets', (req, res) => {
  res.sendFile(path.join(__dirname, '..','Client','src', 'pages', 'myTickets.html'));
})

// user sent a message to flightbot
// app.post('/api/flightbot/:message', (req, res) => {
//   const msg = req.params.message;
//   // process message with AI and send response
//   let Label;
//   let response = analyzeMessage(msg, ());
//   res.send(response);
// })

app.listen(port, () => {
  const host = 'localhost';
  console.log(`Flight Bot listening on http://${host}:${port}`)
})


/** HOW GET WORKS EXPRESS:
 * get(url: string, middleware: function) {
 *    if(REQUESTS_URL == url) {
 *      middleware(REQUEST_OBJECT, RESPONSE_OBJECT);
 *    }
 * }
 */