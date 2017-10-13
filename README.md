# alexa-my-reminders

## dependencies
This skill uses https://github.com/anjishnu/ask-alexa-pykit.
Using pip does not work.
```
git clone https://github.com/anjishnu/ask-alexa-pykit.git
# copy ask folder into project-dir
```

create local Venv for boto3 (if needed)
```
cd alexa-my-reminders
virtualenv venv
source venv/bin/activate

pip install boto3
```

Deploy
`zip -r lambda.zip ./*`