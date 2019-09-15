from app import app, controller #import app object and all default variables
from flask import Flask, flash, redirect, render_template, request, url_for, abort, jsonify, session, make_response
from datetime import datetime
import flask
        
@app.route("/")
def index():
    controller.verifyRefreshInterface(app.config["UPDATE_TIME_INTERVAL"])    
    return render_template("/index.html",\
                           current_date = controller.current_date,\
                           top_newsfeed = controller.top_newsfeed,\
                           latest_newsfeed = controller.latest_newsfeed,\
                           newsfeed = controller.newsfeed)
    
@app.route("/registration")
def registration():
    controller.verifyRefreshInterface(app.config["UPDATE_TIME_INTERVAL"])
        
    response = make_response(render_template("/registration.html", \
                                             current_date = controller.current_date,\
                                            newsfeed = controller.newsfeed,\
                                            top_newsfeed = controller.top_newsfeed,\
                                            latest_newsfeed = controller.latest_newsfeed)), 200
    return response

@app.route("/registration_check", methods=["POST"])
def registration_check():
    if request.method == "POST":
        usr = request.form["username"]
        pwd = request.form["password"]
        pwd2 = request.form["password2"]
        
        if not pwd or not usr or not pwd2:
            abort(400)
        if controller.saveNewAccount(usr,pwd):
            #keep the session about login
            session["USERNAME"] = usr        
            register_success ="Successfully register."
            flash(register_success, "success")    
            response = make_response(render_template("/registration.html", \
                                                     current_date = controller.current_date,\
                                                    newsfeed = controller.newsfeed,\
                                                    top_newsfeed = controller.top_newsfeed,\
                                                    latest_newsfeed=controller.latest_newsfeed)), 200
            return response
        else:
            session.pop("USERNAME", None)
            register_err ="The username does not exist or the password is incorrect."
            flash(register_err, "danger")
            return redirect(url_for('registration'))
    else:
        session.pop("USERNAME", None)
        return redirect(url_for('registration'))
    

    
@app.route("/admin")
def admin():
    controller.verifyRefreshInterface(app.config["UPDATE_TIME_INTERVAL"])        
    response = make_response(render_template("/admin.html", \
                                             current_date = controller.current_date,\
                                            newsfeed = controller.newsfeed,\
                                            top_newsfeed = controller.top_newsfeed,\
                                            latest_newsfeed = controller.latest_newsfeed)), 200
    return response

@app.route("/user_login", methods=["POST"])
def user_login():
    if request.method == "POST":
        pwd = request.form["username"]
        usr = request.form["password"]
        
        if not pwd or not usr:
            abort(400)
        userid = controller.verifyLogin(usr, pwd)
        if userid:
            #keep the session about login
            session["USERNAME"] = usr  
            session["USERID"] = userid  
            if usr in 'admin' and 'admin' in usr:          
                #Other users
                session["isAdmin"] = True
                return redirect(url_for('admin'))
            else:
                #Other users
                return redirect(url_for('index'))
        else:
            session.pop("USERNAME", None)
            login_err ="The username does not exist or the password is incorrect."
            flash(login_err, "danger")
            return redirect(url_for('registration'))
    else:
        session.pop("USERNAME", None)
        return redirect(url_for('registration'))
    
@app.route("/sign_out", methods=["GET", "POST"])
def sign_out():
    session.pop("USERNAME", None)
    session.pop("USERID", None)
    session.pop("isAdmin", None)
    return redirect(url_for('index'))
        

@app.route("/json_page")
def json_page():
    controller.verifyRefreshInterface(app.config["UPDATE_TIME_INTERVAL"])
    return render_template("/json.html", \
                           current_date = controller.current_date,\
                           top_newsfeed = controller.top_newsfeed,\
                           latest_newsfeed=controller.latest_newsfeed)


@app.route('/news', methods=['GET'])
def news():
    controller.verifyRefreshInterface(app.config["UPDATE_TIME_INTERVAL"])
    
    usr = ''
    if session.get('USERNAME'):
        usr = session["USERNAME"]
    if request.method == 'GET' and usr:
        newsid = request.args.get('newsid')
        if newsid:
            newsid = int(newsid)
            newsfeed = controller.getData("News")
            targetnews=newsfeed[newsfeed.newsid == newsid]
            if targetnews.shape[0] > 0:
                title = targetnews["title"].values[0]
                creator = targetnews["creator"].values[0]
                category = targetnews["category"].values[0]
                description =targetnews["description"].values[0]
                pubDate = str(targetnews["pubDate"].values[0])[:10]
                media_url = str(targetnews["media_url"].values[0])
                link = str(targetnews["link"].values[0])
                
                return render_template("/news.html", \
                                                    current_date = controller.current_date,\
                                                    top_newsfeed = controller.top_newsfeed,\
                                                    latest_newsfeed=controller.latest_newsfeed,\
                                                    title = title,creator = creator, \
                                                    category = category,\
                                                    description = description,\
                                                    pubDate = pubDate, media_url = media_url, \
                                                    link = link, newsid = newsid)
    elif not usr:
        login_err = "Please login or register to read the contents."
        flash(login_err, "danger")
        return redirect(url_for("registration"))
    else:
        return redirect(url_for('404', current_date = controller.current_date,\
                           top_news = controller.top_news, newsfeed = controller.newsfeed))



@app.route('/api/v1.0/json/<string:task>', methods=["GET"])
def get_tasks(task):
    if not task:
        abort(404)
    elif task in "latest": 
        return make_response(jsonify(controller.latest_newsfeed.to_dict(orient="index"))), 201
    elif task in "best_rated": 
        return make_response(jsonify(controller.top_newsfeed.to_dict(orient="index"))), 201
    elif task in "all": 
        return make_response(jsonify(controller.newsfeed.to_dict(orient="index"))), 201
    elif task in "interval" and request.method == 'GET' and session.get('USERNAME'):
        start = datetime.strptime(request.args.get('start'), '%Y-%m-%dT%H:%M:%S.%fZ')
        end = datetime.strptime(request.args.get('end'), '%Y-%m-%dT%H:%M:%S.%fZ')
        newsfeed = controller.newsfeed
        respone = newsfeed[(newsfeed['pubDate'] > start) & (controller.newsfeed['pubDate'] <= end)]
        return make_response(jsonify(respone.to_dict(orient="index"))), 201
    else:
        abort(404)        

@app.route('/rating/', methods=["POST"])
def rating():
    #function to get Ajax for rating
    
    userid = ''
    if session.get('USERID'):
        userid = session["USERID"]
        response = request.get_json()
        client_addr = request.environ['REMOTE_ADDR']
        controller.rateNews(response["newsid"], response["rating"], userid, client_addr)
        return make_response(jsonify(response)), 201
    else:
        return make_response(jsonify({"error" : "no user"})), 400
        


@app.route('/limit_interval/', methods=["POST"])
def limit_interval():
    #function to get start and end in python datatime 
    response = request.get_json()
    start = datetime.strptime(response['start'], '%Y-%m-%dT%H:%M:%S.%fZ')
    end = datetime.strptime(response['end'], '%Y-%m-%dT%H:%M:%S.%fZ')
    newsfeed = controller.newsfeed
    newsid_lst = newsfeed[(newsfeed['pubDate'] > start) & (newsfeed['pubDate'] <= end)]["newsid"].tolist()
    response = {"newsid_lst": newsid_lst}
    return make_response(jsonify(response)), 201


@app.errorhandler(400)
def bad_request(e):
    return render_template("/error.html", \
                           current_date = controller.current_date,\
                           top_newsfeed = controller.top_newsfeed,\
                           latest_newsfeed = controller.latest_newsfeed,err='400'), 403

@app.errorhandler(401)
def unauthorized(e):
    return render_template("/error.html", \
                           current_date = controller.current_date,\
                           top_newsfeed = controller.top_newsfeed,\
                           latest_newsfeed = controller.latest_newsfeed,err='403'), 403

@app.errorhandler(403)
def forbidden(e):
    return render_template("/error.html", \
                           current_date = controller.current_date,\
                           top_newsfeed = controller.top_newsfeed,\
                           latest_newsfeed = controller.latest_newsfeed,err='403'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template("/error.html", \
                           current_date = controller.current_date,\
                           top_newsfeed = controller.top_newsfeed,\
                           latest_newsfeed = controller.latest_newsfeed,err='404'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("/error.html", \
                           current_date = controller.current_date,\
                           top_newsfeed = controller.top_newsfeed,\
                           latest_newsfeed=controller.latest_newsfeed, err='500'), 500

