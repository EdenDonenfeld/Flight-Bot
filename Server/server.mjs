import express from "express";
import cors from "cors";

const app = express();
const port = 3000;
app.use(cors());

// user sent a message to flightbot
app.post('/api/flightbot/:message', (req, res) => {
  const msg = req.params.message;
  const modifiedMessage = `FlightBot processed: ${msg}`;
  res.send(modifiedMessage);
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