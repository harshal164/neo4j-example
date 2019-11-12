from flask import Flask, redirect, url_for, request
from neo4j import GraphDatabase
app = Flask(__name__)

class DriverClass:
   def __init__(self, uri, user, password):
      self._driver = GraphDatabase.driver(uri, auth=(user, password))

   def close(self):
      self._driver.close()

   def print_(self, tx,n):
      l = []
      for record in tx.run("MATCH (a:User) where a.name = {n} return a.name,a.age",n=n):
         l.append(({record["a.name"],record["a.age"]}).__repr__())
      return l

   def friend_of(self, tx, n):
      l = []
      for record in tx.run("match (n:User{name:$n})-[:FRIEND_OF]->(m) return m.name,m.age limit 10",n=n):
         print(record)

         l.append([record["m.name"],record["m.age"]].__repr__())
      return l

   def suggestion(self,tx,name):
      l = []
      for record in tx.run("match (suggested:User{name:$n})-[:FRIEND_OF*1..4]->(m)-[:FOLLOWS]->(a)-[:ACTED_IN]->(movie) with collect({name:suggested.name,title:movie.title}) as rows match (suggested:User{name:$n})-[:FRIEND_OF*1..4]->(m)-[:LIKES]->(movie) with rows+collect({name:suggested.name,title:movie.title}) as allrows unwind allrows as row  with row.name as name,row.title as title return name,title,count(*) as c order by c desc", n=name):
         print(record)
         l.append([record["name"], record["title"],record["c"]].__repr__())
      return l

   def call(self,n):
      with self._driver.session() as session:
         return session.read_transaction(self.suggestion,n)

@app.route('/login',methods = ['POST', 'GET'])
def login():
   D = DriverClass("bolt://localhost:7687","neo4j","harshal12")
   if request.method == 'POST':
      user = request.form['nm']
      x = D.call(user)
      return "<br>".join(x)
   else:
      user = request.args.get('nm')
      x = D.call(user)
      return "<br>".join(x)

if __name__ == '__main__':
   app.run(debug = True)