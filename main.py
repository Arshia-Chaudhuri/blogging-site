from flask import Flask, jsonify, render_template, session, redirect, url_for, request
from datetime import timedelta
from functionalities.displayAll import *
from functionalities.createPost import *
from functionalities.signUp import *
from functionalities.login import *
from utils.db import db
from utils.seed import *

SESSION_WILL_BE_VALID = 1 # day

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_management.db'
app.secret_key = 'DebmalyaArshia'
app.permanent_session_lifetime = timedelta(days=SESSION_WILL_BE_VALID)
db.init_app(app)

@app.route('/seed')
def seeding():
    return jsonify(seeding_database())

"""
this function is for displaying all the blog posts on opening the app
"""
@app.route('/')
@app.route('/home')
def home():
    data = display_all()
    print(data)
    return render_template('home.html', data=data, length = len(data))
    # return jsonify(display_all())

"""
this function will help to show the error message to the users
"""
@app.route('/error')
def error():
    return render_template('error.html')

"""
here all login functionalities will be added
"""
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if "userName" in session:
            return redirect(url_for("home"))
        else:
            return render_template('login.html')
    elif request.method == 'POST':
        userName = request.form["username"]
        password = request.form["password"]
        res = log_in(userName, password)
        if res=="SUCCESS":
            return redirect(url_for("home"))
        else:
            return redirect(url_for("error"))
    # return jsonify(log_in())

"""
here all signup functionalities will be added
"""
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method== 'GET':
        if "userName" in session:
            return redirect(url_for("home"))
        else:
            return render_template('signup.html')
    elif request.method == 'POST':
        userName = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        res = sign_up(userName, email, password)
        if res=="SUCCESS":
            return redirect(url_for("home"))
        else:
            return redirect(url_for("error"))
    # return jsonify(sign_up())

"""
jot down all the writing activities
"""
@app.route('/createPost', methods=['POST'])
def create():
    return jsonify(create_post())

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        if "userName" in session:
            return render_template('blog_create.html')
        else:
            return redirect(url_for("home"))
    elif request.method == 'POST':
        pass

"""
blog rendering
"""
@app.route('/blog/<string:blogId>')
def blog(blogId):
    # author,title,body 
    blogs = AllBlogs.query.all()
    print ("*************************************************")
    print (blogs[0].userName)
    for blog in blogs:
        if blog.blogId== blogId:
            userName= blog.userName
            break

    blogDetail= Blog.query.get(blogId)
    title = blogDetail.title
    body = blogDetail.body

    return render_template('blog.html', title=title, author=userName, content=body)


"""
logout
"""
@app.route('/logout')
def logout():
    if "userName" in session:
        session.pop('userName', None)
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(debug=True)