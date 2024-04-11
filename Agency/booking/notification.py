# notifications.py in blog_app directory

from google.auth.transport.requests import Request
from google.oauth2 import service_account
import requests
import json

# We are generating an access_token to be used whenever we want to make a request to FCM
def generate_firebase_auth_key():
    scopes = ['https://www.googleapis.com/auth/firebase.messaging']
    
    
    # Replace the value of credentials_info with what you downloaded from Firebase cloud messaging
    credentials_info = {
        
  
  "type": "service_account",
  "project_id": "viawise-f6bbb",
  "private_key_id": "0a2a7e3677d8c0714720935271272f91a0dff2d2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCn3gmnD6lxjB32\nDVZSIa+TDSbYGs7pdT8IZ4zDagQ6O0IVVfc8QM93N84IqyfxfZIJVUm+VSEXQAnr\ns4clJ7dUrFRBChcDQ+kpTm/xY4jgOuweOqfGuFoLmaLMW7xU5/4UrGHC9GNp69B1\n3IRnT8vrgIuM9S44zYSj08Yrw32EtUk/j7dCP8csdaUPi31/r4uABcGIpTwScf5m\nHZw5nbE+gIXk9Ca39cjOwwAXXqNKcz5infqBTZIsVFOXl7upvFXuDS2FA8QrvcYg\nJijGobhj5XrIbtaxEKEWF/ImimA+Sr0Fkq1pLUlGUhf6XL2oJ9JDe/2mB27/VNS6\n2UTtaMuTAgMBAAECggEAJDRMo6XKly0vlw4oVF1khxQakRgzEQHS/uaKYuj+EWsP\nZRed03Zs6Fr2SkNTwY8iDHZDCdRFZ0TN/vJAzwAiV5Y1M7PP48nlQx3iIc8kSawb\nmadv4PmIniDcDjQoya0hTOcizI+10zXjR1AwlDGPGvMl5dhJSEH2/fhiMLUgYJr4\nsysVvC6I4CvW2jlO7SEYPJGxT9NYb/eYs/RpDuNvKMicI2scaPu3/fYwIX82Xd1l\n8qfrL+16JqQqpS3lrB/yzWIGZvTXF6uQSlbhWTSLxQNBSM5AWe9DIvjQ7zmkSKV/\n7yyz2cF4bjjK0qPsGw9EmudDZbNDCdLcVCTRvFToXQKBgQDo4gX0L5qLcmFgJppN\ne15y3Ml7WLghN2J8AefgxLoG7GbYgPN5AaI6moraWM4wk5nYtsBWzaDCufdqR3+5\nYO+cGc6HITUxzwwoO9xqXpkcsWQ22cH20DMfL+ufdikxjSQXLEaHxPH/fdFEBI0r\nHdLacmSo3OSjd5WHx681560jlwKBgQC4h9najxO7WOo9ktO8NjIw54SUCkKRvo+q\nLELBHHDfVrtl8H2dw11PIG3UMWwp7ACV0gLvL2lJ1/Iema5PyLPS2CtGOd+4/oKU\n1B7J16YioOQPMvAMS0Ktm4R7w/5D3lECel8ZuYsTdCKE/DxtrJ6iarw0qkw/mP3P\ndni2AnhnZQKBgFHlgmCACSI25CWTDbpnwywzlqtI5N/RgVHIvcmehSkAI57JolWQ\njIN9a40jo8cTcQv0IKmmAH3aNjbq0/DWNQ05ShbdR76vaEAR5Q6HG+MqQurDI2Hv\nj7rM+FiIji39y45WpKsESHInxdrcmuRpxYfKqLl1jPYrjKtGPsh/I7UbAoGBALJT\n5v7GIkV9KfGTQTe0EFEejAsc1zRNujy0RVamC5ZqFPPwsxSRRk0/g6P6lxL0VaRz\nrg5D/TY1kHBuB/xmcxGhgkB9kW0P2FXHoHFjC9SPM5ZUnZLj8G4hyqhowgIIiLUi\nWWFc48BLDUkDEcrTdQJ0r6kdok4bpbymOwV54a3ZAoGBAI6Vy4n7UicOHASPyyX2\no3GsHAy31kKH4hBaGYQFxPujfN4uEc/fs/VdUjQgoJ4uneLSWghVK9cNPcm1WrnT\nSWTzn2xmGW/tc+k9seJXkSQJ/p7CEDRA+jwRdttSyoML/lGLKPHo6JCYV6McXGaw\nk6ZESxGWElmRrT/bRpRPyh80\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-vnhtd@viawise-f6bbb.iam.gserviceaccount.com",
  "client_id": "118039979265793632719",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-vnhtd%40viawise-f6bbb.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"


}


    credentials = service_account.Credentials.from_service_account_info(
            credentials_info, scopes=scopes
        )

    credentials.refresh(Request())

    access_token = credentials.token
    return access_token


#this function takes the auth_token(our access_token) and fcm_token(this will be generated from the client side.) as arguments.
# You can customize the message to your preference.
def send_push_notification(auth_token, fcm_token):
    url = "https://fcm.googleapis.com/v1/projects/testpush-8c6ea/messages:send"

    payload = json.dumps({
    "message": {
        "token": f'{fcm_token}',
        "notification": {
        "title": "New blog published!",
        "body": "Hey, There is a new blog post you might want to check out."
        },
        "data": {
        "key1": "value1",
        "key2": "value2"
        }
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {auth_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
