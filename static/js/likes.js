document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const eventId = this.dataset.eventId;
            const isAuthenticated = this.dataset.liked === 'true';
            
            if (!isAuthenticated) {
                alert('Please log in to like events');
                return;
            }
            
            // Get CSRF token from cookie
            const csrftoken = getCookie('csrftoken');
            
            fetch(`/home/like/${eventId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.message === 'Liked') {
                    this.classList.add('liked', 'bxs-heart');
                    this.classList.remove('bx-heart');
                } else if (data.message === 'Unliked') {
                    this.classList.remove('liked', 'bxs-heart');
                    this.classList.add('bx-heart');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while processing your request. Please try again.');
            });
        });
    });
});

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 