from communityForum import app, db
from flask import render_template, request, redirect, url_for
from communityForum.forms import UserInfoForm, LoginForm, PostForm, CommentForm
from communityForum.models import User, Post, check_password_hash, Comment
from flask_login import login_required, login_user, current_user, logout_user

@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', user_posts = posts)

@app.route('/test')
def testRoute():
    names = ['Robert','David','Bill','Jessy']
    return render_template('test.html',list_names = names)
    #adding context to this template, this context is going to be names

@app.route('/register', methods = ['GET','POST'])
def register():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        print(username,email,password)

        user = User(username,email,password)

        db.session.add(user)

        db.session.commit()

    return render_template('register.html', user_form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()

        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', login_form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/posts', methods = ['GET', 'POST'])
@login_required
def posts():
    form = PostForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        post = Post(title,content,user_id)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('forumPost.html', post_form = form)

@app.route('/posts/<int:post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('forumPostDetail.html', post = post)

@app.route('/posts/update/<int:post_id>', methods = ['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id

        post.title = title
        post.content = content
        post.user_id = user_id

        db.session.commit()
        return redirect(url_for('home'))
    return render_template('forumPostUpdate.html', update_form = form)

@app.route('/posts/comment/<int:post_id>', methods=['GET','POST'])
@login_required
def post_comment(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.all()
    form = CommentForm()

    if request.method == 'POST' and form.validate():
        text = form.text.data
        user_id = current_user.id
        comment = Comment(text,user_id)


        db.session.add(comment)
        db.session.commit()
        
        # for comment in Comment.query.order_by(Comment.timestamp.asc()):
        #     print('{}: {}'.format(comment.author, comment.text))
        return redirect(url_for('home'))
    return render_template('forumPostComment.html', comment_form = form)
    

@app.route('/posts/delete/<int:post_id>', methods = ['GET','POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))