from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Comment, Tag
from .database import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    return redirect(url_for('auth.login'))

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    # Add new note
    if request.method == 'POST' and not request.args.get('partial'):
        note_data = request.form.get('note')
        tag_string = request.form.get('tags')

        if len(note_data) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note_data, user_id=current_user.id)

            if tag_string:
                tag_names = [t.strip().lower() for t in tag_string.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                    new_note.tags.append(tag)

            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            return redirect(url_for('views.home'))

    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date.desc()).all()
    notes_with_comments = [(note, len(note.comments)) for note in notes]

    # If partial param is present, render new note form only (for adding new note panel)
    if request.args.get('partial') == 'new_note_form':
        return render_template('partials/new_note_form.html')

    return render_template("home.html", user=current_user, notes_with_comments=notes_with_comments)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@views.route('/edit-note/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)

    if note.user_id != current_user.id:
        flash('You are not authorized to edit this note.', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        note_data = request.form.get('note')  # <-- fixed variable name from new_data to note_data
        tag_string = request.form.get('tags')

        if not note_data or len(note_data.strip()) < 1:
            flash('Note is too short!', category='error')
        else:
            note.data = note_data
            note.tags.clear()

            if tag_string:
                tag_names = [t.strip().lower() for t in tag_string.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                    note.tags.append(tag)

            db.session.commit()
            flash('Note updated!', category='success')

            if request.args.get('partial'):
                return jsonify({'success': True})

            return redirect(url_for('views.home'))

    if request.args.get('partial'):
        return render_template('partials/edit_note_partial.html', user=current_user, note=note)

    return render_template("edit_note.html", user=current_user, note=note)



@views.route('/note/<int:id>', methods=['GET', 'POST'])
@login_required
def view_note(id):
    note = Note.query.get_or_404(id)

    if note.user_id != current_user.id:
        flash('Unauthorized', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        comment_text = request.form.get('comment')
        if comment_text:
            new_comment = Comment(text=comment_text, user_id=current_user.id, note_id=note.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added!', category='success')
        else:
            flash('Comment cannot be empty.', category='error')

    comments = Comment.query.filter_by(note_id=note.id).all()

    # ✅ Fix placement — avoid NoneType error for both full and partial renders
    if not note.data:
        note.data = ''

    if request.args.get('partial'):
        return render_template('partials/view_note_partial.html', user=current_user, note=note, comments=comments)

    return render_template('view_note.html', user=current_user, note=note, comments=comments)
@views.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html', user=current_user)
