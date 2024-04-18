#Python
import json
import time

 
def prepareResponse(event, msgText, intentState):
    response = {
          "sessionState": {
            "dialogAction": {
              "type": "Close"
            },
            "intent": {
              "name": event['sessionState']['intent']['name'],
                  "state": intentState
            }
          },
          "messages": [
           {
             "contentType": "PlainText",
             "content": msgText
            }
           ]
       }
     
    return response
 
def cancelIceCreamOrder(event):
    # Your order cancelation code here
    msgText = "Order has been canceled"
    return prepareResponse(event, msgText, "Fulfilled")

def fallbackRepresentative(event):
    # Connecting to a representative
    time.sleep(2.5)
    msgText = "Thank you for chatting with PG today. I am unable to help with your inquiry today. We are connecting to you a representative.  They will be with you shortly.  Have an amazing day!"
    return prepareResponse(event, msgText, "Failed")
 
def createIceCreamOrder(event):
      
     firstName = event['sessionState']['intent']['slots']['name']['value']['interpretedValue']
     iceCreamFlavor = event['sessionState']['intent']['slots']['flavor']['value']['interpretedValue']
     iceCreamSize = event['sessionState']['intent']['slots']['size']['value']['interpretedValue']
      
     print(firstName, iceCreamFlavor, iceCreamSize)
      
     discount = event['sessionState']['sessionAttributes']['discount']
      
     #print('Discount: ', discount)
      
     # Your custom order creation code here.
      
     msgText = "Your Order for, " + str(iceCreamSize) + " " + str(iceCreamFlavor) + " IceCream has been placed with Order#: 342342"
 
     return prepareResponse(event, msgText, "Fulfilled")   
      
     
def lambda_handler(event, context):
    intentName = event['sessionState']['intent']['name']
    response = None
         
    if intentName == 'CreateOrderIntent':
        response = createIceCreamOrder(event)
    elif intentName == 'CancelOrderIntent':
        response = cancelIceCreamOrder(event)
    elif intentName == 'FallbackIntent':
        response = fallbackRepresentative(event)
    else: 
        raise Exception('The intent : ' + intentName + ' is not supported')
    return response
