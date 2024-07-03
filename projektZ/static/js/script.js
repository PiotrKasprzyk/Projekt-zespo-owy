document.addEventListener('DOMContentLoaded', function() {
    const replyToggles = document.querySelectorAll('.toggle-reply-form');

    replyToggles.forEach(toggle => {
        toggle.addEventListener('click', function(event) {
            event.preventDefault();
            const commentId = this.getAttribute('data-comment-id');
            const replyForm = document.getElementById(`reply-form-${commentId}`);
            if (replyForm.style.display === 'none' || replyForm.style.display === '') {
                replyForm.style.display = 'block';
            } else {
                replyForm.style.display = 'none';
            }
        });
    });
});
