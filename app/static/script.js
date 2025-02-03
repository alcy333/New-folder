document.addEventListener('DOMContentLoaded', () => {
    // Update countdown timers
    function updateTimers() {
        document.querySelectorAll('.countdown').forEach(el => {
            const endTime = new Date(el.dataset.end);
            const now = new Date();
            const diff = endTime - now;

            if (diff <= 0) {
                el.textContent = 'Expired';
                return;
            }

            const hours = Math.floor(diff / (1000 * 60 * 60));
            const minutes = Math.floor((diff / (1000 * 60)) % 60);
            el.textContent = `${hours}h ${minutes}m left`;
        });
    }
    setInterval(updateTimers, 60000);
    updateTimers();

    // WebSocket connection
    const socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.product_id) {
            const priceEl = document.querySelector(`#price-${data.product_id}`);
            if (priceEl) {
                priceEl.textContent = `$${data.new_price.toFixed(2)}`;
            }
        }
    };

    // Suggest bid handler
    document.querySelectorAll('.suggest-bid').forEach(button => {
        button.addEventListener('click', async () => {
            const productId = button.dataset.productId;
            const response = await fetch(`/bids/suggest/${productId}`);
            const data = await response.json();
            document.querySelector(`#amount-${productId}`).value = data.suggested;
        });
    });
});