from boofuzz import *

session = Session(
    target=Target(connection=TCPSocketConnection("127.0.0.1",8021))
)

user = Request("user",children=)