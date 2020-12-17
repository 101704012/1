from flask import Flask,render_template,request
import redis
import random 
app = Flask(__name__)
random.seed()

r = redis.Redis(host='localhost', port=6379, db=0)


a = 0
print (a)
@app.route('/longtoshot/', methods=['GET', 'POST'])
def hello():
    global a
    if request.method == 'POST':
         lurl = request.form['longurl']
         
         print (lurl)
         ttl = request.form['ttltime']
         
         #surl = request.form['shorturl']
         surl=random.randint(127643, 999999)
         print (surl)
         r.set(surl,lurl.encode('utf-8'))
         if int(ttl) > 0:
             r.expire(surl,ttl)
              
         #print(shurl)
         print(r.get(surl))
         return render_template('json.html',longurl = lurl,shorturl = surl,ttltime = ttl )
    else:
         return render_template('json.html',longurl = '',shorturl = '',ttltime=0 )


@app.route('/shottolong/', methods=['GET', 'POST'])
def shottolng():
    global a
    if request.method == 'POST':
         surl = request.form['shorturl']
         print (surl)
         print (surl)
    
         #lurl = str(r.get(surl))
         if len(str(r.get(surl))) > 4:
              lurl = r.get(surl).decode('utf-8')
         else:
              lurl = r.get(surl)           

         ttl=r.ttl(surl)     
         print(lurl)
         print(ttl)
         #r.flushall
         return render_template('json2.html',longurl = lurl,shorturl = surl,ttltime = ttl )
         
    else:
         return render_template('json2.html',longurl = '',shorturl = '',ttltime=0 )



#background process happening without any refreshing
@app.route('/background_process_test1')
def background_process_test1():
    global a
    a = a + 10
    print (a)
    r.flushall()
    return "nothing"

@app.route('/background_process_test2')
def background_process_test2():
    global a
    a = a - 1
    print (a)
    return "nothing"




if __name__ == '__main__':
    app.debug = True
    app.run()

