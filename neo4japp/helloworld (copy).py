from flask import Flask
from neo4j import GraphDatabase
app = Flask(__name__)
class DriverLifecycleExample:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_(self,tx):
        l = []
        for record in tx.run("MATCH (a:User) return a.name"):
            l.append(record["a.name"])
        return l
    def call(self):
        with self._driver.session() as session:
            return session.read_transaction(self.print_)

@app.route('/')
def main():
    D = DriverLifecycleExample("bolt://localhost:7687","neo4j","harshal12")
    l = D.call()
    D.close()
    s="<br>".join(l)
    return "<h1>"+s+"</h1>"
app.run(debug=True)
#
#
#
#
#
#
#
#
# def hello_world():
#    return 'Hello World’
#
# if __name__ == '__main__':
#    app.run()