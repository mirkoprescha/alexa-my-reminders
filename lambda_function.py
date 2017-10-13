from ask import alexa
import read_reminders
from config import APPLICATION_ID, S3_BUCKET, S3_KEY

def lambda_handler(request_obj, context=None):
    print "S3 Config is bucket {} with key {}".format(S3_BUCKET, S3_KEY)

    if request_obj['session']['application']['applicationId'] != APPLICATION_ID:
        raise ValueError("Invalid Application ID")

    return alexa.route_request(request_obj)


@alexa.default
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request type """
    return alexa.respond('Starte mit Spiele meine Erinnerungen ab.')


@alexa.request("LaunchRequest")
def launch_request_handler(request):
    ''' Handler for LaunchRequest '''
    return alexa.create_response(message="Hallo und willkommen zu meine Erinnerungen.")


@alexa.request("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Auf Wiedersehen!")


@alexa.intent('ReadMyRemindersIntent')
def read_my_reminders_intent_handler(request):
    print "starting intent {} for user_id {} and session_id {}".format(request.intent_name(), request.user_id(), request.session_id())
    my_reminder_text = read_reminders.getTextFromS3(S3_BUCKET, S3_KEY)
    cleaned_reminders = read_reminders.clean_text(my_reminder_text)
    ssml = read_reminders.generate_ssml(cleaned_reminders)
    #return alexa.create_response("Hier sind deine Erinnerungen. {}".format(cleaned_reminders), end_session=True, is_ssml=True)
    return alexa.create_response(ssml, end_session=True, is_ssml=True)


if __name__ == "__main__":    
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--serve','-s', action='store_true', default=False)
    args = parser.parse_args()
    
    if args.serve:        
        ###
        # This will only be run if you try to run the server in local mode 
        ##
        print('Serving ASK functionality locally.')
        import flask
        server = flask.Flask(__name__)
        @server.route('/')
        def alexa_skills_kit_requests():
            request_obj = flask.request.get_json()
            return lambda_handler(request_obj)
        server.run()
