function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/notes";
  });
}
function loadNoteView(noteId) {
  fetch(`/note/${noteId}`)
    .then((res) => res.text())
    .then((html) => {
      document.querySelector(".note-editor").innerHTML = html;
    });
}

function loadNoteEdit(noteId) {
  fetch(`/edit-note/${noteId}`)
    .then((res) => res.text())
    .then((html) => {
      document.querySelector(".note-editor").innerHTML = html;
    });
}

function loadHome() {
  window.location.href = "{{ url_for('views.home') }}";
}
