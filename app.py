from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "digital_scam_project_2026"

# Home Page
@app.route('/')
def home():
    return render_template('home.html')


# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        session['user'] = email

        return redirect('/dashboard')

    return render_template('login.html')


# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('scam.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# User Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('scam.db')

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reports")

    total_reports = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM reports ORDER BY id DESC LIMIT 5")

    recent_reports = cursor.fetchall()
    pending_reports = total_reports
    resolved_reports = 0
    awareness_posts = 3

    conn.close()

    return render_template(
    "dashboard.html",
    total_reports=total_reports,
    pending_reports=pending_reports,
    resolved_reports=resolved_reports,
    awareness_posts=awareness_posts,
    recent_reports=recent_reports
    )

# Awareness Page
@app.route('/awareness')
def awareness():
    return render_template('awareness.html')


# Report Scam
@app.route('/report', methods=['GET', 'POST'])
def report():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        scamtype = request.form['scamtype']

        conn = sqlite3.connect('scam.db')
        cursor = conn.cursor()

        status = "Pending"

        cursor.execute(
        """
        INSERT INTO reports
        (name, email, phone, scamtype, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, email, phone, scamtype, status)

        )

        conn.commit()
        conn.close()

        return "Scam Report Submitted Successfully"

    return render_template('report.html')


# View Reports
@app.route('/view_reports')
def view_reports():

    conn = sqlite3.connect('scam.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports")

    reports = cursor.fetchall()

    conn.close()

    return render_template('view_reports.html', reports=reports)


# Search Reports
@app.route('/search', methods=['GET', 'POST'])
def search():

    reports = []

    if request.method == 'POST':

        keyword = request.form['keyword']

        conn = sqlite3.connect('scam.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM reports WHERE scamtype LIKE ?",
            ('%' + keyword + '%',)
        )

        reports = cursor.fetchall()

        conn.close()

    return render_template('search.html', reports=reports)


# Admin Login
@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            return redirect('/admin_dashboard')

        return "Invalid Admin Login"

    return render_template('admin_login.html')


# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():

    conn = sqlite3.connect('scam.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reports")

    total_reports = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'admin_dashboard.html',
        total_reports=total_reports
    )

# Edit Report
@app.route('/edit_report/<int:id>', methods=['GET', 'POST'])
def edit_report(id):

    conn = sqlite3.connect('scam.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        scamtype = request.form['scamtype']

        cursor.execute(
            '''
            UPDATE reports
            SET name=?, email=?, phone=?, scamtype=?
            WHERE id=?
            ''',
            (name, email, phone, scamtype, id)
        )

        conn.commit()
        conn.close()

        return redirect('/view_reports')

    cursor.execute(
        "SELECT * FROM reports WHERE id=?",
        (id,)
    )

    report = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_report.html',
        report=report
    )


# Delete Report
@app.route('/delete_report/<int:id>')
def delete_report(id):

    conn = sqlite3.connect('scam.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reports WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/view_reports')

#update_status
@app.route('/update_status/<int:id>', methods=['GET', 'POST'])
def update_status(id):

    conn = sqlite3.connect('scam.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        status = request.form['status']

        cursor.execute(
            "UPDATE reports SET status=? WHERE id=?",
            (status, id)
        )

        conn.commit()
        conn.close()

        return redirect('/view_reports')

    cursor.execute(
        "SELECT * FROM reports WHERE id=?",
        (id,)
    )

    report = cursor.fetchone()

    conn.close()

    return render_template(
        'update_status.html',
        report=report
    )

#check_status
@app.route('/check_status', methods=['GET', 'POST'])
def check_status():

    report = None

    if request.method == 'POST':

        email = request.form['email']

        conn = sqlite3.connect('scam.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM reports WHERE email=?",
            (email,)
        )

        report = cursor.fetchone()

        conn.close()

    return render_template(
        'check_status.html',
        report=report
    )

#feedback
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = sqlite3.connect('scam.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

        return "Feedback Submitted Successfully"

    return render_template('feedback.html')


#view_feedback
@app.route('/view_feedback')
def view_feedback():

    conn = sqlite3.connect('scam.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM feedback")

    feedbacks = cursor.fetchall()

    conn.close()

    return render_template(
        'view_feedback.html',
        feedbacks=feedbacks
    )


#news
@app.route('/news')
def news():
    return render_template('news.html')


#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#profile
@app.route('/profile')
def profile():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('scam.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (session['user'],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user
    )


# Edit Profile
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('scam.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute("""
            UPDATE users
            SET name=?, email=?, phone=?
            WHERE email=?
        """, (name, email, phone, session['user']))

        conn.commit()

        # Update session email if user changed it
        session['user'] = email

        conn.close()

        return redirect('/profile')

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (session['user'],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_profile.html',
        user=user
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
#if __name__ == '__main__':
  #  app.run(debug=False)
