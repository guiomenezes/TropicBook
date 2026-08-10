const token = localStorage.getItem("token");

if (!token) {
    window.location.href = '../index.html';
}

loadDashboard();

async function loadDashboard() {

    try {

        const response = await fetch(
            'http://127.0.0.1:8000/reports/dashboard',
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (response.status === 401){

            localStorage.removeItem('token');
            window.location.href = '../index.html';
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to load dashboard data.");
        }

        const data = await response.json();

        document.getElementById("total-guests").textContent = 
            data.total_guests;

        document.getElementById("active-rooms").textContent = 
            data.active_rooms;
        
        document.getElementById("active-reservations").textContent =
            data.active_reservations;

        document.getElementById('monthly-revenue').textContent = 
            `$${Number(data.monthly_revenue).toFixed(2)}`;

        loadRecentReservations(data.recent_reservations);
    }

    catch (error) {

        console.error(error);
        alert('Unable to load dashboard.');
    }

}

function loadRecentReservations(reservations) {

    const tbody = document.getElementById('recent-reservations');

    tbody.innerHTML = "";

    reservations.forEach(reservation => {

        tbody.innerHTML += `
        <tr>
            <td>${reservation.guest}</td>
            <td>${reservation.room}</td>
            <td>${reservation.check_in}</td>
            <td>${reservation.check_out}</td>
        </tr>
        `;
    });
}

document.getElementById('logout-btn').addEventListener('click', () => {
    
    localStorage.removeItem('token');

    window.location.href = '../index.html';

});