const token = localStorage.getItem("token")

// Check authentication
if (!token) {
    window.location.href = "../index.html";
}

// Load guest when page opens
loadGuests();

// Load guests

async function loadGuests() {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/guests/",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        // Token expired or invalid
        if (response.status === 401) {

            localStorage.removeItem("token");

            window.location.href = "../index.html";

            return;
        }

        const guests = await response.json();

        renderGuests(guests);
    }

    catch (error) {

        console.error(error);

        alert("Unable to load guests.")
    }
}

// Render Guests

function renderGuests(guests) {

    const tbody = document.getElementById('guests-table');

    tbody.innerHTML = '';

    guests.forEach(guest => {

        tbody.innerHTML += `
        <tr>
            <td>${guest.id}</td>

            <td>${guest.name}</td>

            <td>${guest.last_name}</td>

            <td>${guest.document ?? ""}</td>

            <td>${guest.phone ?? ""}</td>

            <td>${guest.email ?? ""}</td>

            <td>

                <button 
                    onclick="deleteGuest(${guest.id})">
                    Delete
                </button>

            </td>

        </tr>

        `;
    });
}

// ===============================
// CREATE GUEST
// ===============================

document
    .getElementById("guest-form")
    .addEventListener("submit", async (event) => {

        event.preventDefault();


        const guest = {

            name:
                document.getElementById("name").value,

            last_name:
                document.getElementById("last_name").value,

            document:
                document.getElementById("document").value || null,

            phone:
                document.getElementById("phone").value || null,

            email:
                document.getElementById("email").value || null

        };


        try {

            const response = await fetch(
                "http://127.0.0.1:8000/guests/",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${token}`

                    },

                    body: JSON.stringify(guest)

                }
            );


            if (response.status === 401) {

                localStorage.removeItem("token");

                window.location.href =
                    "../index.html";

                return;
            }


            if (!response.ok) {

                const data =
                    await response.json();

                document.getElementById(
                    "error-message"
                ).textContent =
                    data.detail || "Unable to create guest.";

                return;
            }


            // Clear form
            document
                .getElementById("guest-form")
                .reset();


            document.getElementById(
                "error-message"
            ).textContent = "";


            // Reload list
            loadGuests();

        }

        catch (error) {

            console.error(error);

            alert("Unable to create guest.");

        }

    });


// ===============================
// DELETE GUEST
// ===============================

async function deleteGuest(guestId) {

    const confirmed =
        confirm("Are you sure you want to delete this guest?");


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(

            `http://127.0.0.1:8000/guests/${guestId}`,

            {

                method: "DELETE",

                headers: {

                    Authorization:
                        `Bearer ${token}`

                }

            }

        );


        if (response.status === 401) {

            localStorage.removeItem("token");

            window.location.href =
                "../index.html";

            return;
        }


        if (!response.ok) {

            const data =
                await response.json();

            alert(
                data.detail ||
                "Unable to delete guest."
            );

            return;
        }


        // Reload guest list
        loadGuests();

    }

    catch (error) {

        console.error(error);

        alert("Unable to delete guest.");

    }

}


// ===============================
// LOGOUT
// ===============================

document
    .getElementById("logout-btn")
    .addEventListener("click", () => {

        localStorage.removeItem("token");

        window.location.href =
            "../index.html";

    });