#Python
import json
import time

def lambda_handler(event, context):
    intentName = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']
    bot = event['bot']['name']
    response = None
         
    if intentName == 'FallbackIntent':
        response = fallbackRepresentative(event)
    elif intentName == 'MakeAPayment':
        response = makeAPayment(event, slots)
    else: 
        raise Exception('The intent : ' + intentName + ' is not supported')
    return response

def makeAPayment(event, slots):
    makeAPayment_slot_validation_result = makeAPaymentSlotValidation(event, slots)

    print('after validation step')
    if event['invocationSource'] == 'DialogCodeHook':
        print('insided dialogcodehook step')
        if not makeAPayment_slot_validation_result['isValid']:
            print('MakeAPayment slot(s) are invalid')
            if 'message' in makeAPayment_slot_validation_result:
                print('MakeAPayment slot(s) are invalid with a message')
                return prepareResponseDialogCodeHookWithMessage(event, slots, makeAPayment_slot_validation_result)
            else:
                print('MakeAPayment slot(s) are invalid with NO message, just empty slots')
                return prepareResponseDialogCodeHook(event, slots, makeAPayment_slot_validation_result)
        else:
            print('MakeAPayment slot(s) are valid and delegating to next step')
            return prepareResponseDelegage(event, slots)

    if event['invocationSource'] == 'FulfillmentCodeHook':
        print('MakeAPayment slot(s) are valie, fulfilled complete.')
        msgTxt = 'Processed your payment, successfully.'
        return prepareResponseClose(event, msgText, "Fulfilled")

def makeAPaymentSlotValidation(event, slots):
    print ('Validating slots for MakeAPayment intent')
    print (slots)
    if not slots['LoanNumber']:
        print ('LoanNumber Slot is empty')
        return {
            'isValid': False,
            'invalidSlot': 'LoanNumber'
        }
    if not slots['LoanNumber']['value']['originalValue'].isnumeric():
        print ('LoanNumber not numeric')
        return {
            'isValid': False,
            'invalidSlot': 'LoanNumber',
            'message': 'LoanNumber must be in a numberica value'
        }
    if not slots ['MortgagePayment']:
        print('MortgagePayment slot is empty')
        return { 
            'isValid': False,
            'invalidSlot': 'MortgagePayment'
        }
    if not slots['MortgagePayment']['value']['originalValue'].isnumeric():
        print ('MortgagePayment not numeric')
        return {
            'isValid': False,
            'invalidSlot': 'MortgagePayment',
            'message': 'MortgagePayment must be in a numberica value'
        }

    return {'isValid': True}

def fallbackRepresentative(event):
    # Connecting to a representative
    time.sleep(2.5)
    msgText = "Thank you for chatting with PG today. I am unable to help with your inquiry today. We are connecting to you a representative.  They will be with you shortly.  Have an amazing day!"
    return prepareResponseClose(event, msgText, "Failed")

def cancelIceCreamOrder(event):
    # Your order cancelation code here
    msgText = "Order has been canceled"
    return prepareResponse(event, msgText, "Fulfilled")
 
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

def prepareResponseClose(event, msgText, intentState):
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

def prepareResponseDelegage(event, slots):
    response = {
          "sessionState": {
            "dialogAction": {
              "type": "Delegate"
            },
            "intent": {
                "name": event['sessionState']['intent']['name'],
                "slots": slots
            }
          }
       }
     
    return response

def prepareResponseDialogCodeHook(event, slots, validation_result):
    response = {
          "sessionState": {
            "dialogAction": {
              "slotToElicit": validation_result['invalidSlot'],
              "type": "ElicitSlot"
            },
            "intent": {
                "name": event['sessionState']['intent']['name'],
                "slots": slots
            }
          }
       }
     
    return response

def prepareResponseDialogCodeHookWithMessage(event, slots, validation_result):
    response = {
          "sessionState": {
            "dialogAction": {
              "slotToElicit": validation_result['invalidSlot'],
              "type": "ElicitSlot"
            },
            "intent": {
                "name": event['sessionState']['intent']['name'],
                "slots": slots
            }
          },
          "messages": [
           {
             "contentType": "PlainText",
             "content": validation_result['message']
            }
           ]
       }
     
    return response
