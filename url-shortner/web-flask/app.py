from flask import Flask,render_template,request
from send import direct_bp
from check_url import register_url
app=Flask(__name__)
app.register_blueprint(direct_bp,url_prefix='/d')

@app.route("/",methods=["GET","POST"])
def home():
    h_url="None"
    if request.method=="POST":
        url=request.form.get("url")
        h_url="http://localhost/d/"
        u_cod=register_url(url)
        h_url=h_url+u_cod
        return render_template("index.html",h_url=h_url)
    return render_template("index.html",h_url=h_url)

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
