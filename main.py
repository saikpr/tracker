
#example.com/image?id=test
#example.com is our domain
#image is the webpage we are trying to access
#id is the HTTP GET argument we are passing to the URL
#test is the value of id we are passing to URL


# Import the Flask Framework
from flask import Flask,request,send_file
# Import the ndb google datastore library
from google.appengine.ext import ndb

import logging

#importing function to push a notification to pushbullet account
from imagedwnl.pushbullet import push_to_pushbullet
#configuration data
from imagedwnl.config import data_dict

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


#We create a ndb model, with 2 attributes
class imageTrack(ndb.Model):
    image_id = ndb.StringProperty() #example 'test' in example.com/image?id=test
    count = ndb.IntegerProperty()

#we create another model with 4 attribute
class info_events(ndb.Model):
    image_id = ndb.StringProperty()
    remote_addr = ndb.StringProperty()
    headers = ndb.StringProperty()
    user_Agent = ndb.StringProperty()

#adding route to /image URI
@app.route('/image')
def hello():
    """gets the image id, creates 2 entities
    one which maintains the count of how many times the imagewith id tag is accessed
    and another to store the HTTP headers
    """
    #get image_id form the HTTP GET
    image_id = request.args.get('id')

    if image_id != None:
        this_response = info_events(image_id=image_id,#id accessed
                                remote_addr=request.remote_addr, #remote ip address
                                headers=str(request.headers),#headers
                                user_Agent = str(request.headers.get('User-Agent')))#user agent
        this_response.put()  #saving it on Google DATASTORE
        #query if image_id is already in database
        find_image_id = imageTrack.query(imageTrack.image_id == image_id )

        logging.info('Checking '+str(image_id))

        if find_image_id.get() == None:
            #if image_id is not in datastore
            logging.info('Not Found, Pushing '+str(image_id))
            #create a new object
            this_el = imageTrack(image_id =str(image_id),count = 1 )
            
            logging.info('Putting '+str(this_el.image_id)+" with count 1")
            this_el.put() #saving it
        else :
            #get the image_id entity
            this_el = find_image_id.fetch(1)[0]
            this_el.count = this_el.count +1
            logging.info('Found '+str(this_el.image_id)+" with count "+str(this_el.count))
            this_el.put()#saving it

    push_to_pushbullet(data_dict,"Got Visit","Visit at "+this_el.image_id+" from "+str(request.remote_addr))       
    #returning a dot png(1 pixel)
    return send_file("dot.png", mimetype='image/png')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

if __name__ == "__main__":
    app.run(debug=True)
