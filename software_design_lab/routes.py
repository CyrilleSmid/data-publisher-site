from flask import render_template, url_for, flash, redirect, request, session, abort
from software_design_lab import app, db, bcrypt
from software_design_lab.forms import RegistrationFormUser, RegistrationFormAuthor, LoginForm, PublishForm, UpdateAccountForm, UpdatePublicationForm
from software_design_lab.models import User, Author, PublicationTopic, Publication
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import secrets
import os
from software_design_lab.topic_model.abstract_extractor import read_first_page, extract_abstract_text
import openai
from api_keys import API_KEY
from software_design_lab.topic_model.topic_model import KerasNNTopicModelFactory, KerasNNTopicModel
openai.api_key = API_KEY

@app.route('/')
@app.route('/home')
def index():
    # db.create_all()
    # print(db.engine.table_names())

    # import pandas as pd
    # from software_design_lab.models import User, Author, PublicationTopic, Publication
    # df = pd.read_csv("C:\dev\Projects\software-design-lab\software_design_lab\databases\Tags.csv")
    # for i, topic_name in df.iterrows():
    #     topic = PublicationTopic(i, topic_name["Tags"])
    #     db.session.add(topic)
    # db.session.commit()

    publications = Publication.query.order_by(Publication.upload_date.desc()).all()
    return render_template("index.html", publications=publications, title='Home')

@app.route('/about')
def about():
    return render_template("about.html", title='About')

def save_user(form):
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(first_name=form.first_name.data,
                surname=form.surname.data,
                email=form.email.data,
                registration_date=datetime.utcnow(),
                password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationFormUser()
    if form.validate_on_submit():
        user = save_user(form)
        flash(f'User account created for {form.first_name.data} {form.surname.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register_base.html', title='Register User', form=form)
@app.route('/register_author', methods=['GET', 'POST'])
def register_author():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationFormAuthor()
    if form.validate_on_submit():
        user = save_user(form)
        author = Author(user_id=user.id)
        db.session.add(author)
        db.session.commit()
        flash(f'Author account created for {form.first_name.data} {form.surname.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register_base.html', title='Register Author', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            author = Author.query.filter_by(id=user.id).first()
            if author: session['login_type'] = 'author'
            else: session['login_type'] = 'user'
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.surname = form.surname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.surname.data = current_user.surname
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


def save_publication(form_doc):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_doc.filename)
    doc_fn = random_hex + f_ext
    doc_path = os.path.join(app.root_path, 'frontend/static/publications', doc_fn)

    form_doc.save(doc_path)
    return doc_path, doc_fn

@app.route("/publication/new", methods=['GET', 'POST'])
@login_required
def new_publication():
    form = PublishForm()
    if session['login_type'] != 'author':
        return redirect(url_for('index'))
    if form.validate_on_submit():
        doc_path, doc_fn = save_publication(form.publication_pdf.data)

        first_page = read_first_page(doc_path).replace('  ', ' ').replace('\n', ' ')
        prompt = 'Extract the full abstract from this publication text:\n' + first_page
        abstract = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=500)['choices'][0]['text']
        abstract = abstract.replace('  ', ' ')
        abstract = abstract.replace('\n', ' ')
        abstract = abstract.replace('Abstract: ', '').strip()
        prompt = 'Explain this like I am 12. After that, explain it in the most pretentious, hard to read and overly complicated and convoluted way possible. After that, explain it in a confused and exaggerated manner. Format it as follows: (Like I am 12:, Overly complicated:, Confused:):' + abstract
        simple_desc = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=500)['choices'][0]['text']
        simple_desc = simple_desc.replace('  ', ' ').strip()
        # simple_desc = simple_desc.replace('\n', ' ')
        # abstract = """This study aims to understand the relationship between scientific writing and scientific impact by analyzing linguistic complexity in full-text Biology and Psychology articles. Linguistic complexity is measured using 12 variables and the scientific impact of the articles is grouped into high, medium, and low categories. The results show no significant relationship between linguistic complexity and citation strata in either discipline, suggesting that textual complexity plays little role in scientific impact in the data sets. The study also discusses other factors that may affect scientific impact, such as publication venues, review cycles, and collaboration."""
        factory = KerasNNTopicModelFactory()
        model = factory.get_topic_model()
        topic_id = int(model.predict_topic(abstract))

        publication = Publication(
            title=form.title.data,
            thumbnail='default.jpg',
            abstract=abstract, 
            simple_desc=simple_desc,
            topic_id=topic_id, 
            upload_date=datetime.utcnow(),
            publication_file= doc_fn,
            author_id=current_user.id,
            article_authors=form.article_authors.data
        )
        db.session.add(publication)
        db.session.commit()
        flash('Your article has been published', 'sucess')
        return redirect(url_for('index'))
    return render_template('publish.html', title='Publish', form=form)

@app.route("/publication/<int:publication_id>")
def publication(publication_id):
    publication = Publication.query.get_or_404(publication_id)
    return render_template('publication.html', title=publication.title, publication=publication)

@app.route("/publication/<int:publication_id>/update", methods=['GET', 'POST'])
@login_required
def update_publication(publication_id):
    publication = Publication.query.get_or_404(publication_id)
    if publication.author.id != current_user.id:
        abort(403)
    form = UpdatePublicationForm()
    if form.validate_on_submit():
        publication.title = form.title.data
        publication.article_authors = form.article_authors.data
        publication.abstract = form.abstract.data
        publication.simple_desc = form.simple_desc.data
        db.session.commit()
        flash('Your publication has been updated!', 'success')
        return redirect(url_for('publication', publication_id=publication.id))
    elif request.method == 'GET':
        form.title.data = publication.title
        form.article_authors.data = publication.article_authors
        form.abstract.data = publication.abstract
        form.simple_desc.data = publication.simple_desc
    return render_template('update_publication.html', title=publication.title, form=form, publication=publication)

@app.route("/publication/<int:publication_id>/delete", methods=['GET','POST'])
@login_required
def delete_publication(publication_id):
    publication = Publication.query.get_or_404(publication_id)
    if publication.author.id != current_user.id:
        abort(403)
    file_path = os.path.join(app.root_path, 'frontend/static/publications', publication.publication_file)
    if os.path.exists(file_path):
        os.remove(file_path)
        print("Removed publication at: ", file_path)
    else:
        print("The file does not exist")
    db.session.delete(publication)
    db.session.commit()
    flash('Your publication has been deleted!', 'success')
    return redirect(url_for('index'))