#!/usr/bin/env bash
zip -r lambda.zip ./*
aws lambda update-function-code --function-name alexa-my-reminders --zip-file fileb://lambda.zip