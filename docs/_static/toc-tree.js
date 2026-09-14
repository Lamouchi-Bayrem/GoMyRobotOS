/* GoMyRobotOS documentation navigation.
 *
 * Sphinx renders the full toctree (every section under its caption, all
 * pages, all in-page subsections) into this menu. Each "caption + list"
 * pair is turned into a <details> group so that:
 *   - all top-level sections are visible at once,
 *   - clicking a section name selects it (visual accent) and opens/closes
 *     the list of what is under it,
 *   - the section containing the page you are reading starts open.
 * No theme files are modified; the markup transformation happens here,
 * in the page's own DOM, per page.
 */
(function () {
  "use strict";

  function init() {
    var menu = document.querySelector(
      '.wy-menu-vertical[role="navigation"]'
    );
    if (!menu || menu.getAttribute("data-gmros-toc") === "applied") {
      return;
    }
    menu.setAttribute("data-gmros-toc", "applied");

    var captions = menu.querySelectorAll("p.caption");
    Array.prototype.forEach.call(captions, function (caption) {
      var list = caption.nextElementSibling;
      if (!list || list.tagName !== "UL") {
        return; /* not a navigation section (e.g. footer captions) */
      }

      var group = document.createElement("details");
      group.className = "gmros-section";

      var toggle = document.createElement("summary");
      toggle.className = "gmros-section-toggle";
      var label = caption.querySelector(".caption-text");
      toggle.appendChild(label ? label : caption.cloneNode(true));

      /* The list is moved into the group; the caption is replaced by it. */
      group.appendChild(toggle);
      group.appendChild(list);

      var isCurrent = list.querySelector("li.current") !== null;
      if (isCurrent) {
        group.setAttribute("open", "");
        toggle.classList.add("is-current");
      }
      toggle.addEventListener("click", function () {
        /* Fired after the native toggle changes <details open>. */
        toggle.classList.toggle("is-current", group.hasAttribute("open"));
      });

      menu.replaceChild(group, caption);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();