from flask import Flask , request , render_template , session , redirect , url_for , flash


app = Flask(__name__)

#creating a secret key for session cookie
app.secret_key = "My secret key"

#user database

users_db = {}


# Route for the homepage
@app.route("/")
def index():
    #Check if a user is logged in
    if "username" in session:
        username = session["username"]
        # Get user-specific data
        user_info = users_db.get(username)
        return render_template("index.html" , username=username , email=user_info["email"])
    
    # Return url for login if not in session
    return redirect(url_for("login"))



# Route for logging in 
@app.route("/login" , methods = ["GET" , "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        #Check if the username and password match
        user = users_db.get(username)
        if user and user["password"] == password:
            #Store username in the session
            session["username"] = username
            flash("Login successful" , "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password" , "danger")

    return render_template("login.html")


# Route for registration page
@app.route("/register" , methods = ["GET" , "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]


        #Check if the user already exists
        if username in users_db:
            flash("Username already exists. PLease choose another one." , "danger")
            return redirect(url_for("register"))
        
        #Add the new user to the simulated database
        users_db[username] = {"username": username, "password": password, "email": email}
        flash("Registration successful! You can now log in", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")


#Route for logging out
@app.route("/logout")
def logout():
    # Remove the username from the session (logout the user)
    session.pop("username",None)
    flash("You have been logged out" , "info")
    return redirect(url_for("login"))





if __name__ == "__main__":
    app.run(port=8080 , debug=True)