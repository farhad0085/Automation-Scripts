from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///database.db')

Base = declarative_base()

class Response(Base):
    __tablename__ = 'response'

    id = Column(Integer, primary_key=True)
    response = Column(String)


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    body = Column(String)
    created_at = Column(String)
    symbol = Column(String)

    response_id = Column(Integer, ForeignKey('response.id'))
    response = relationship("Response", back_populates="message")

Response.message = relationship("Message", order_by=Message.id, back_populates="response")
Base.metadata.create_all(engine)

def get_prev_data_from_db(symbol):
    Session = sessionmaker(bind=engine)
    session = Session()

    bodies = []

    for m in session.query(Message).filter(Message.symbol == symbol).all():
        bodies.append(m.body)

    return bodies

def get_all_data_from_db():
    Session = sessionmaker(bind=engine)
    session = Session()

    output = []

    for m, r in session.query(Message, Response).filter(Message.response_id==Response.id).all():
        dict = {}
        dict['respone'] = r.response
        dict['username'] = m.username
        dict['body'] = m.body
        dict['created_at'] = m.created_at
        dict['symbol'] = m.symbol

        output.append(dict)

    return output

if __name__ == "__main__":
    bodies = get_prev_data_from_db("AAPL")
    print(bodies)