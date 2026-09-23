let selectedSeat = null;
let schedulesData = [];
let currentBasePrice = 0.0;

async function loadMovies() 
{
    const res = await fetch('/api/movies');
    const movies = await res.json();
    const tbody = document.getElementById('movies-table-body');
    tbody.innerHTML = '';

    movies.forEach(movie => 
    {
        tbody.innerHTML += `<tr>
            <td>${movie.id}</td>
            <td>${movie.title}</td>
            <td>${movie.genre}</td>
            <td>$${movie.price.toFixed(2)}</td>
            <td>${movie.duration_mins} mins</td>
        </tr>`;
    });
}

async function loadSchedules() 
{
    const res = await fetch('/api/schedules');
    schedulesData = await res.json();
    
    const tbody = document.getElementById('schedules-table-body');
    const dropdown = document.getElementById('schedule-dropdown');
    
    tbody.innerHTML = '';
    dropdown.innerHTML = '';

    schedulesData.forEach(sch => 
    {
        tbody.innerHTML += `<tr>
            <td>${sch.id}</td>
            <td>${sch.title}</td>
            <td>Hall ${sch.hall_number}</td>
            <td>${sch.showtime}</td>
        </tr>`;

        dropdown.innerHTML += `<option value="${sch.id}">
            Schedule #${sch.id}: ${sch.title} ($${sch.price.toFixed(2)})
        </option>`;
    });

    onScheduleChange();
}

function onScheduleChange() 
{
    const selectedId = parseInt(document.getElementById('schedule-dropdown').value);
    const schedule = schedulesData.find(s => s.id === selectedId);
    
    if(schedule) 
    {
        currentBasePrice = schedule.price;
        selectedSeat = null;
        document.getElementById('selected-seat-text').textContent = 'None';
        updatePriceSummary();
        renderSeats(selectedId);
    }
}

function updatePriceSummary() 
{
    const ageInput = parseInt(document.getElementById('age-input').value) || 20;
    
    let discountPercent = 0;
    let finalTotal = currentBasePrice;

    if(ageInput < 18) 
    {
        discountPercent = 10;
        finalTotal *= 0.90;
    }

    document.getElementById('price-base').textContent = `$${currentBasePrice.toFixed(2)}`;
    document.getElementById('price-discount').textContent = discountPercent > 0 ? `10% Youth Off` : `None (0%)`;
    document.getElementById('price-total').textContent = `$${finalTotal.toFixed(2)}`;
}

async function renderSeats(scheduleId) 
{
    const response = await fetch(`/api/seats?schedule_id=${scheduleId}`);
    const seats = await response.json();
    
    const container = document.getElementById('seat-container');
    container.innerHTML = '';

    seats.forEach(seat => 
    {
        const btn = document.createElement('button');
        const rowLetter = String.fromCharCode(64 + seat.row_num);
        const seatName = `${rowLetter}${seat.col_num}`;
        
        btn.textContent = seatName;
        btn.className = 'seat-btn';

        if(seat.is_booked === 1) 
        {
            btn.style.backgroundColor = '#dc3545'; 
            btn.disabled = true;
        } 
        
        else 
        {
            btn.style.backgroundColor = '#28a745'; 
            
            btn.onclick = () => 
            {
                document.querySelectorAll('.seat-btn').forEach(b => 
                {
                    if(!b.disabled) b.style.backgroundColor = '#28a745';
                });

                btn.style.backgroundColor = '#007bff'; 
                selectedSeat = {row: seat.row_num, col: seat.col_num, name: seatName};
                document.getElementById('selected-seat-text').textContent = seatName;
            };
        }
        
        container.appendChild(btn);
    });
}

async function buyTicket() 
{
    if(!selectedSeat) 
    {
        alert('Please click on an available seat first!');
        return;
    }

    const scheduleId = parseInt(document.getElementById('schedule-dropdown').value);
    const age = document.getElementById('age-input').value;
    const amount = document.getElementById('pay-input').value;

    if(!age || !amount) 
    {
        alert('Please enter your age and payment amount.');
        return;
    }

    const response = await fetch('/api/buy-ticket', 
    {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify
        ({
            schedule_id: scheduleId,
            row_num: selectedSeat.row,
            col_num: selectedSeat.col,
            age: parseInt(age),
            amount_paid: parseFloat(amount)
        })
    });

    const result = await response.json();

    if(result.success) 
    {
        alert(`${result.message}\nTotal Charged: $${result.price.toFixed(2)}\nChange Returned: $${result.change.toFixed(2)}`);
        onScheduleChange(); 
    } 
    
    else 
    {
        alert(`Error: ${result.message}`);
    }
}

document.addEventListener('DOMContentLoaded', () => 
{
    loadMovies();
    loadSchedules();
});