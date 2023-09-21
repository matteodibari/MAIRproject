while(1):
    sentence = input()
    output = 'inform'
    if 'bye' in sentence:
        output = 'bye'
    if 'goodbye' in sentence:
        output = 'bye'
    if 'yes' in sentence:
        output = 'affirm'
    if 'right' in sentence:
        output = 'affirm'
    if 'confirm' in sentence:
        output = 'affirm'
    if 'no ' in sentence:
        output = 'negate'
    if sentence == 'not':
        output = 'negate'
    if 'hi ' in sentence:
        output = 'hello'
    if 'hello' in sentence:
        output = 'hello'
    if 'more' in sentence:
        output = 'reqmore'
    if 'how about' in sentence:
        output = 'reqalts'
    if 'anything else' in sentence:
        output = 'reqalts'
    if 'start over' in sentence:
        output = 'restart'
    if 'repeat' in sentence:
        output = 'restart'
    if 'reset' in sentence:
        output = 'restart'
    if 'thank' in sentence:
        output = 'thankyou'
    if 'dont want' in sentence:
        output = 'deny'
    if 'wrong' in sentence:
        output = 'deny'
    if sentence == 'cough':
        output = 'null'
    if sentence == 'unintelligible':
        output = 'null'
    if sentence == 'sil':
        output = 'null'
    if 'is it ' in sentence:
        output = 'confirm'
    if 'does it ' in sentence:
        output = 'confirm'
    if 'what' in sentence:
        output = 'request'
    if 'which' in sentence:
        output = 'request'
    if 'when' in sentence:
        output = 'request'
    if 'phone' in sentence:
        output = 'request'
    if 'address' in sentence:
        output = 'request'
    if 'price' in sentence:
        output = 'request'
    print(output)