from ask import alexa

def lambda_handler(request_obj, context=None):

    from config import APPLICATION_ID
    if request_obj['session']['application']['applicationId'] != APPLICATION_ID:
        raise ValueError("Invalid Application ID")



    metadata = {'user_name' : 'SomeRandomDude'} # add your own metadata to the request using key value pairs
    
    ''' inject user relevant metadata into the request if you want to, here.    
    e.g. Something like : 
    ... metadata = {'user_name' : some_database.query_user_name(request.get_user_id())}

    Then in the handler function you can do something like -
    ... return alexa.create_response('Hello there {}!'.format(request.metadata['user_name']))
    '''
    return alexa.route_request(request_obj, metadata)


@alexa.default
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request type """
    return alexa.respond('Just ask').with_card('Hello World')


@alexa.request("LaunchRequest")
def launch_request_handler(request):
    ''' Handler for LaunchRequest '''
    return alexa.create_response(message="Hello Welcome to My Recipes!")


@alexa.request("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")


@alexa.intent('GetRecipeIntent')
def get_recipe_intent_handler(request):
    """
    You can insert arbitrary business logic code here    
    """

    # Get variables like userId, slots, intent name etc from the 'Request' object
    ingredient = request.slots["Ingredient"]  # Gets an Ingredient Slot from the Request object.
    
    if ingredient == None:
        return alexa.create_response("Could not find an ingredient!")

    # All manipulations to the request's session object are automatically reflected in the request returned to Amazon.
    # For e.g. This statement adds a new session attribute (automatically returned with the response) storing the
    # Last seen ingredient value in the 'last_ingredient' key. 

    request.session['last_ingredient'] = ingredient # Automatically returned as a sessionAttribute
    
    # Modifying state like this saves us from explicitly having to return Session objects after every response

    # alexa can also build cards which can be sent as part of the response
    card = alexa.create_card(title="GetRecipeIntent activated", subtitle=None,
                             content="asked alexa to find a recipe using {}".format(ingredient))    

    return alexa.create_response("Finding a recipe with the ingredient {}".format(ingredient),
                                 end_session=False, card_obj=card)



@alexa.intent('NextRecipeIntent')
def next_recipe_intent_handler(request):
    """
    You can insert arbitrary business logic code here
    """
    return alexa.create_response(message="Getting Next Recipe ... 123")


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
    
