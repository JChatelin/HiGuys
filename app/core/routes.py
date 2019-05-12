from flask import render_template, flash, request, redirect, url_for
from app.core import bp
from app import db
from flask_login import login_required, current_user
from app.core.forms import EditProfileForm, PostForm
from datetime import datetime
from app.models import User, Post


@bp.route('/', methods=['POST', 'GET'])
@bp.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    form = PostForm()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('core.index'))
    return render_template('core/index.html', title='Home', form=form, posts=posts)


@bp.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('core/index.html', title='Explore', posts=posts)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('core/user.html', title="Profile", user=user, posts=posts)


@bp.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for('core.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('core/edit_profile.html', title="Edit Profile", form=form)


@bp.route('/user/<username>/follow')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user == current_user:
        flash('You cannot follow yourself.')
        return redirect(url_for('core.user', username=current_user.username))
    if user is None:
        flash('User {} not found.'.format(user.username))
        return redirect(url_for('core.index'))
    current_user.follow(user)
    db.session.commit()
    return redirect(url_for('core.user', username=user.username))


@bp.route('/user/<username>/unfollow')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user == current_user:
        flash('You cannot unfollow yourself.')
        return redirect(url_for('core.user', username=current_user.username))
    if user is None:
        flash('User {} not found.'.format(user.username))
        return redirect(url_for('core.index'))
    current_user.unfollow(user)
    db.session.commit()
    return redirect(url_for('core.user', username=user.username))