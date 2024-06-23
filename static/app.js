document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('tap-button').addEventListener('click', function() {
        fetch('/tap', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                document.getElementById('balance').innerText = data.new_balance;
            } else {
                alert(data.message);
            }
        });
    });

    document.getElementById('boost-tap').addEventListener('click', function() {
        fetch('/boost_tap', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert('Tap capacity boosted!');
                location.reload();
            } else {
                alert(data.message);
            }
        });
    });

    document.getElementById('boost-storage').addEventListener('click', function() {
        fetch('/boost_storage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert('Storage capacity boosted!');
                location.reload();
            } else {
                alert(data.message);
            }
        });
    });

    document.getElementById('boost-recharge-speed').addEventListener('click', function() {
        fetch('/boost_recharge_speed', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert('Recharge speed boosted!');
                location.reload();
            } else {
                alert(data.message);
            }
        });
    });

    document.getElementById('claim-referral-rewards').addEventListener('click', function() {
        fetch('/referral_rewards', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert(`You have received ${data.rewards} points!`);
                location.reload();
            } else {
                alert(data.message);
            }
        });
    });

    document.getElementById('update-theme').addEventListener('change', function() {
        const newTheme = document.getElementById('update-theme').value;
        fetch('/update_theme', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ theme: newTheme })
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert('Theme updated!');
                location.reload();
            } else {
                alert(data.message);
            }
        });
    });
});
