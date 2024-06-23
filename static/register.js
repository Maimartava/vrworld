document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('register-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(event.target);
        const data = {
            email: formData.get('email'),
            username: formData.get('username'),
            password: formData.get('password')
        };

        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert('Registration successful! Please check your email to confirm your account.');
                window.location.href = '/login';
            } else {
                alert(data.message);
            }
        });
    });
});
