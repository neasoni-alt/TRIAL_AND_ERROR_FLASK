from .database import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Association table for many-to-many relationship between Note and Tag
note_tags = db.Table(
    'note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(db.Model):
    """
    Tag model represents tags that can be assigned to notes.
    Each tag has a unique name.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag {self.name}>'

class Note(db.Model):
    """
    Note model represents a note created by a user.
    Contains the note content, timestamp, and relations to user and tags.
    """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))  # Note content
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Owner user ID
    comments = db.relationship('Comment', backref='note', cascade='all, delete-orphan', lazy=True)

    # Many-to-many relationship with Tag via note_tags association table
    tags = db.relationship(
        'Tag',
        secondary=note_tags,
        lazy='subquery',
        backref=db.backref('notes', lazy=True)
    )

class User(db.Model, UserMixin):
    """
    User model represents the users of the application.
    Includes email, password, first name, and relationships to notes and comments.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    # One-to-many relationship: a user can have multiple notes
    notes = db.relationship('Note', backref='user', lazy=True)

    # One-to-many relationship: a user can have multiple comments
    comments = db.relationship('Comment', backref='user', lazy=True)

class Comment(db.Model):
    """
    Comment model represents comments on notes.
    Each comment is linked to one note and one user.
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now())
