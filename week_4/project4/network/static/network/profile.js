document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('h5').forEach(function(profile) {
        profile.onclick = function() {
            console.log('Hi');
        }
    });
})