#Python
import json
import time

def lambda_handler(event, context):
    intentName = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']
    response = None
         
    if intentName == 'FallbackIntent':
        response = fallbackRepresentativeIntent(event)
    elif intentName == 'MakeAPayment':
        response = makeAPaymentIntent(event, slots)
    elif intentName == 'PayoffMortgage':
        response = payoffMortgageIntent(event, slots)
    else: 
        raise Exception('The intent : ' + intentName + ' is not supported')
    return response

## Start MakeAPayment Intent

def makeAPaymentIntent(event, slots):
    makeAPayment_slot_validation_result = makeAPaymentSlotValidation(event, slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not makeAPayment_slot_validation_result['isValid']:
            if 'message' in makeAPayment_slot_validation_result:
                return prepareResponseDialogCodeHookWithMessage(event, slots, makeAPayment_slot_validation_result)
            else:
                return prepareResponseDialogCodeHook(event, slots, makeAPayment_slot_validation_result)
        else:
            return prepareResponseDelegage(event, slots)

    if event['invocationSource'] == 'FulfillmentCodeHook':
        msgTxt = 'Processed your payment, successfully.'
        return prepareResponseClose(event, msgText, "Fulfilled")

def makeAPaymentSlotValidation(event, slots):
    loanNumberValidationResult = loanNumberValidation(event, slots)

    if not loanNumberValidationResult['isValid']:
        return loanNumberValidationResult

    if not slots ['MortgagePayment']:
        return { 
            'isValid': False,
            'invalidSlot': 'MortgagePayment'
        }
    if not slots['MortgagePayment']['value']['originalValue'].isnumeric():
        return {
            'isValid': False,
            'invalidSlot': 'MortgagePayment',
            'message': 'MortgagePayment must be in a numeric value'
        }

    return {'isValid': True}

## End MakeAPayment Intent

## Start PayoffMortgage Intent

def payoffMortgageIntent(event, slots):
    payoffMortgage_slot_validation_result = payoffMortgageSlotValidation(event, slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not payoffMortgage_slot_validation_result['isValid']:
            if 'message' in payoffMortgage_slot_validation_result:
                return prepareResponseDialogCodeHookWithMessage(event, slots, payoffMortgage_slot_validation_result)
            else:
                return prepareResponseDialogCodeHook(event, slots, payoffMortgage_slot_validation_result)
        else:
            return prepareResponseDelegage(event, slots)

    if event['invocationSource'] == 'FulfillmentCodeHook':
        msgTxt = 'Processed your payoff, successfully!  You are debt free!!!!'
        return prepareResponseClose(event, msgText, "Fulfilled")

def payoffMortgageSlotValidation(event, slots):
    return loanNumberValidation(event, slots)

## End PayoffMortgage Intent

## Start FallBack Intent

def fallbackRepresentativeIntent(event):
    # Connecting to a representative
    time.sleep(2.5)
    msgText = "Thank you for chatting with PG today. I am unable to help with your inquiry today. We are connecting to you a representative.  They will be with you shortly.  Have an amazing day!"
    return prepareResponseClose(event, msgText, "Failed")

## End FallBack Intent

## Start Helper Methods

def loanNumberValidation(event, slots):
    if not slots['LoanNumber']:
        return {
            'isValid': False,
            'invalidSlot': 'LoanNumber'
        }
    if not slots['LoanNumber']['value']['originalValue'].isnumeric():
        return {
            'isValid': False,
            'invalidSlot': 'LoanNumber',
            'message': 'LoanNumber must be in a numeric value'
        }
    return {'isValid': True}

## End Helper Methods

## Start Response Helper  

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

## End Response Helper
