(function ($) {
    "use strict";

    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 40) {
            $('.navbar').addClass('sticky-top');
        } else {
            $('.navbar').removeClass('sticky-top');
        }
    });
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });


    // Modal Video
    $(document).ready(function () {
        var $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });
        console.log($videoSrc);

        $('#videoModal').on('shown.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })

        $('#videoModal').on('hide.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc);
        })
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


   // Facts counter
if (typeof $.fn.counterUp === "function") {
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });
}

// Testimonials carousel
if (typeof $.fn.owlCarousel === "function") {
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        margin: 45,
        dots: true,
        loop: true,
        center: true,
        responsive: {
            0: { items: 1 },
            576: { items: 1 },
            768: { items: 2 },
            992: { items: 3 }
        }
    });
}
    
})(jQuery);

/* =====================================
   FOODZONE SIDE DRAWER FUNCTIONALITY
===================================== */

document.addEventListener("DOMContentLoaded", function () {
    const trigger = document.getElementById("fzMenuTrigger");
    const drawer = document.getElementById("fzSideDrawer");
    const overlay = document.getElementById("fzDrawerOverlay");
    const closeButton = document.getElementById("fzDrawerClose");

    // Drawer elements are not present on every page yet.
    if (!trigger || !drawer || !overlay || !closeButton) {
        return;
    }

    function openDrawer() {
        document.body.classList.add("fz-drawer-open");
        trigger.setAttribute("aria-expanded", "true");
        drawer.setAttribute("aria-hidden", "false");
        closeButton.focus();
    }

    function closeDrawer() {
        document.body.classList.remove("fz-drawer-open");
        trigger.setAttribute("aria-expanded", "false");
        drawer.setAttribute("aria-hidden", "true");
        trigger.focus();
    }

    trigger.addEventListener("click", openDrawer);
    closeButton.addEventListener("click", closeDrawer);
    overlay.addEventListener("click", closeDrawer);

    document.addEventListener("keydown", function (event) {
        if (
            event.key === "Escape" &&
            document.body.classList.contains("fz-drawer-open")
        ) {
            closeDrawer();
        }
    });
});