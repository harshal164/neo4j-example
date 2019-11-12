from flask import Flask
from neo4j import GraphDatabase
app = Flask(__name__)

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