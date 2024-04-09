import express from "express";
import cors from "cors";
import {analyzeMessage} from "./analyze.mjs";

const app = express();
const port = 3000;
app.use(cors());

// user sent a message to flightbot
app.post('/api/flightbot/:message', (req, res) => {
  const msg = req.params.message;
  // process message with AI and send response
  let Label;
  let response = analyzeMessage(msg, ());
  res.send(response);
})

app.listen(port, () => {
  console.log(`Flight Bot listening on port ${port}`)
})


/** HOW GET WORKS EXPRESS:
 * get(url: string, middleware: function) {
 *    if(REQUESTS_URL == url) {
 *      middleware(REQUEST_OBJECT, RESPONSE_OBJECT);
 *    }
 * }
 */