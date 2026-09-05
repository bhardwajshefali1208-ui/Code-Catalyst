document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if (form) {

        form.addEventListener("submit", function () {

            const button = form.querySelector("button");

            if (button) {

                button.innerHTML = "ANALYZING TRANSACTION...";

                button.disabled = true;

            }

        });

    }


    /*
     * Automatically refresh dashboard
     * every 30 seconds when no filters
     * are being used.
     */

    const isDashboard =
        window.location.pathname === "/dashboard";

    const hasFilters =
        window.location.search.length > 0;


    if (isDashboard && !hasFilters) {

        setTimeout(function () {

            window.location.reload();

        }, 30000);

    }

});