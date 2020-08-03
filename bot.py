import requests
from db_helper import Message, Response, engine, get_prev_data_from_db
from sqlalchemy.orm import sessionmaker

CLIENT_ID = "9fa2b8f4e81cc1c8"
CLIENT_SECRET = "acfa1edd26c3a94bd4b3ef288654ce7a07ab734c"

def get_messages(endpoint, symbol):

    final_output = {}
    output = []

    endpoint = f"{endpoint}/{symbol}.json"

    try:
        response = requests.get(endpoint).json()
    except:
        print("Could not get response")
        return None

    if response['response']['status'] != 200:
        print("Code not found")
        return None

    for message in response['messages']:
        message_dict = {'username': message['user']['username'], 'body': message['body'],
                        'created_at': message['created_at'], 'symbol': message['symbols'][0]['symbol']}
        output.append(message_dict)

    final_output['messages'] = output
    final_output['response'] = response

    return final_output


def save_to_db(messages):
    response = str(messages['response'])

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        new_resp = Response(response=response)
        session.add(new_resp)
        session.commit()

        for message in messages['messages']:
            username = message['username']
            body = message['body']
            created_at = message['created_at']
            symbol = message['symbol']

            new_msg = Message(username=username,
                              body=body,
                              created_at=created_at,
                              symbol=symbol,
                              response_id=new_resp.id)
            session.add(new_msg)

            session.commit()
    except:
        return False
    return True


def get_fresh_new_data(new_data, query):
    old_data = get_prev_data_from_db(query)

    if len(old_data) == 0:
        return new_data

    new_dict = {}
    output = []
    new_dict['response'] = new_data['response']

    for message in new_data['messages']:
        match = 0

        for data in old_data:
            if message['body'] == data:
                match = 1
                break

        if not match:
            my_dict = {}
            my_dict['username'] = message['username']
            my_dict['body'] = message['body']
            my_dict['created_at'] = message['created_at']
            my_dict['symbol'] = message['symbol']
            output.append(my_dict)

    new_dict['messages'] = output

    return new_dict

if __name__ == "__main__":
    symbol = "AAPL"
    endpoint = "https://api.stocktwits.com/api/2/streams/symbol"

    messages = get_messages(endpoint, symbol)

    new_messages = get_fresh_new_data(messages, symbol)
    save_to_db(new_messages)