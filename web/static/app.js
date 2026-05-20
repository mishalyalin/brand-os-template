/* Brand OS - minimal client-side behavior.
   The interface is server-rendered. This file only handles:
   - autofocus the search box on the index page
   - submit on Cmd/Ctrl+Enter from the search box
   - graceful no-op if JS is disabled
*/

(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        var searchInput = document.querySelector("input.search-input");
        if (searchInput && !searchInput.value) {
            searchInput.focus();
        }

        // Cmd/Ctrl+Enter shortcut
        document.addEventListener("keydown", function (e) {
            if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
                var form = document.querySelector("form.search-form-element");
                if (form) {
                    form.submit();
                }
            }
        });

        // Surface internal nav links with a copy-permalink behavior on h2/h3 hover.
        // Intentionally lightweight - no library, no anchors mutation.
    });
})();
