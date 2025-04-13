function togglePasswordModal() {
    document.querySelectorAll('.modal.show').forEach(modal => {
        var bootstrapModal = bootstrap.Modal.getInstance(modal);
        if (bootstrapModal) {
            bootstrapModal.hide();
        }
    });
    var passwordModal = new bootstrap.Modal(document.getElementById("enter-password"))
    var passwordInput = document.getElementById("password-input")
    document.getElementById("enter-password").addEventListener("shown.bs.modal", () => {
        passwordInput.focus();
    }, { once: true }); // Use { once: true } to ensure this listener is called only once

    passwordModal.toggle();

}

let inactivityTimeout;

function resetInactivityTimer() {
    clearTimeout(inactivityTimeout);

    inactivityTimeout = setTimeout(() => {
        // Trigger HTMX manually
        htmx.trigger(htmx.find("#content"), "inactivity");
        console.log('This function triggeres in 5 seconds!')
        togglePasswordModal()
    }, 480000); // 5 seconds of inactivity
}

// Reset timer on user activity
["mousemove", "keydown", "click", "scroll"].forEach(event => {
    document.addEventListener(event, resetInactivityTimer);
});

// Start the timer initially
resetInactivityTimer();

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('shown.bs.modal', () => {
            const firstInput = modal.querySelector('.first-input');
            if (firstInput) {
                firstInput.focus();
            }

        });
    });
});



/*
<script data-cfasync="false" src="{% static 'app/js/email-decode.min.js' %}"></script> 
<script src="{% static 'app/js/vendor.min.js' %}" type="14876ca369a8ef5d0d48d13e-text/javascript"></script>
<script src="{% static 'app/js/app.min.js' %}" type="14876ca369a8ef5d0d48d13e-text/javascript"></script>


<script src="{% static 'app/plugins/jvectormap-next/jquery-jvectormap.min.js' %}"
type="14876ca369a8ef5d0d48d13e-text/javascript"></script>
<script src="{% static 'app/plugins/jvectormap-content/world-mill.js' %}"
    type="14876ca369a8ef5d0d48d13e-text/javascript"></script>
    <script src="{% static 'app/plugins/apexcharts/dist/apexcharts.min.js' %}"
    type="14876ca369a8ef5d0d48d13e-text/javascript"></script>
    <script src="{% static 'app/js/demo/dashboard.demo.js' %}" type="14876ca369a8ef5d0d48d13e-text/javascript"></script>

    <script async src="https://www.googletagmanager.com/gtag/js?id=G-Y3Q0VGQKY3"
    type="14876ca369a8ef5d0d48d13e-text/javascript"></script>
<script type="14876ca369a8ef5d0d48d13e-text/javascript">
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    
    gtag('config', 'G-Y3Q0VGQKY3');
</script>
<script src="{% static 'app/js/rocket-loader.min.js' %}" data-cf-settings="14876ca369a8ef5d0d48d13e-|49" defer></script>
*/