const token = localStorage.getItem('token');

async function loadRooms() {

    const response = await fetch(
        'http://127.0.0.1:8000/rooms',
        {
            headers: {
                Authorization: 'Bearer ${token}'
            }
        }
    )
    
};

const rooms = await response.json();

const container = document.getElementById('rooms-container');

rooms.forEach(room => {
    const div = document.createElement('div');

    div.innerHTML = `
        <h3>${room.name}</h3>
        <p>Capacidade: ${room.capacity}</p>
        <p>Preço: R$ ${room.price}</p>
        `;

        container.appendChild(div);
    
    });

loadRooms();