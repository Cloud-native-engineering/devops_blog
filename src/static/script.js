document.addEventListener('DOMContentLoaded', function() {
    const deleteBtn = document.getElementById('delete-btn');
    const editPostForm = document.getElementById('edit-post-form');
    const newPostForm = document.getElementById('new-post-form');

    if (deleteBtn) {
        deleteBtn.addEventListener('click', function() {
            const postId = window.location.pathname.split('/').pop();
            fetch(`/post/${postId}`, {
                method: 'DELETE'
            }).then(response => {
                if (response.ok) {
                    window.location.href = '/';
                } else {
                    alert('Error deleting post');
                }
            });
        });
    }

    if (editPostForm) {
        editPostForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = document.getElementById('post-id').value;
            const title = document.getElementById('title').value;
            const content = document.getElementById('content').value;
            fetch(`/post/${postId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, content })
            }).then(response => {
                if (response.ok) {
                    window.location.href = `/post/${postId}`;
                } else {
                    alert('Error updating post');
                }
            });
        });
    }

    if (newPostForm) {
        newPostForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const title = document.getElementById('title').value;
            const content = document.getElementById('content').value;
            fetch('/new-post', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ title, content })
            }).then(response => {
                if (response.ok) {
                    window.location.href = '/';
                } else {
                    alert('Error creating post');
                }
            });
        });
    }
});
