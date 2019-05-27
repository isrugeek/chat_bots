const express = require('express');
const bodyParser = require('body-parser');
//const verificationController = require('./controllers/verification');
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.listen(9000, () => console.log('Air-bel Bot is starting working , port 9000'));
//app.get('/', verificationController);

const verificationController = require('./controllers/verification');
const messageWebhookController = require('./controllers/messageWebhook');
app.get('/', verificationController);
app.post('/', messageWebhookController);
