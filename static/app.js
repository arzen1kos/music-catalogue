(() => {
  document.addEventListener("click", (e) => {
    const t = e.target;
    if (!(t instanceof Element)) return;

    const legacyBurger = t.closest("#mobile-burger");
    if (legacyBurger) {
      e.preventDefault();
      const menu = document.getElementById("mobile-menu");
      if (menu) {
        menu.style.display = menu.style.display === "none" || !menu.style.display ? "block" : "none";
      }
      return;
    }

    const burger = t.closest("[data-burger]");
    if (burger) {
      e.preventDefault();
      const menu = document.querySelector("[data-mobile-menu]");
      const expanded = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", expanded ? "false" : "true");
      if (menu) {
        menu.hidden = expanded;
      }
      return;
    }

    const modalClose = t.closest("[data-modal-close]");
    if (modalClose) {
      e.preventDefault();
      closeModal();
      return;
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
  });

  // Close legacy mobile menu when a link is clicked
  document.addEventListener("click", (e) => {
    const t = e.target;
    if (!(t instanceof Element)) return;
    if (t.closest("#mobile-menu .mobile-item")) {
      const menu = document.getElementById("mobile-menu");
      if (menu) menu.style.display = "none";
    }
  });

  function closeModal() {
    const modal = document.querySelector("[data-modal]");
    if (!modal) return;
    modal.hidden = true;
    modal.setAttribute("aria-hidden", "true");
    modal.dataset.open = "false";
    const foot = modal.querySelector("[data-modal-foot]");
    if (foot) foot.innerHTML = "";
  }

  function openModal({ title, body, footHtml }) {
    const modal = document.querySelector("[data-modal]");
    if (!modal) return;
    const titleEl = modal.querySelector("[data-modal-title]");
    const bodyEl = modal.querySelector("[data-modal-body]");
    const footEl = modal.querySelector("[data-modal-foot]");
    if (titleEl) titleEl.textContent = title || "Confirm";
    if (bodyEl) bodyEl.innerHTML = body || "";
    if (footEl) footEl.innerHTML = footHtml || "";
    modal.hidden = false;
    modal.setAttribute("aria-hidden", "false");
    modal.dataset.open = "true";
  }

  // Delete confirmation modals (POST-only forms)
  document.addEventListener("submit", (e) => {
    const form = e.target;
    if (!(form instanceof HTMLFormElement)) return;

    const kind = form.dataset.confirmKind;
    if (!kind) return;

    // already confirmed
    if (form.dataset.confirmed === "true") return;

    e.preventDefault();

    const label = form.dataset.confirmLabel || "this item";
    const danger = form.dataset.confirmDanger || "Delete";

    openModal({
      title: "Confirm deletion",
      body: `<p>Delete <strong>${escapeHtml(label)}</strong>? This cannot be undone.</p>`,
      footHtml: `
        <button class="btn btn--ghost" type="button" data-modal-close>Cancel</button>
        <button class="btn btn--danger" type="button" data-confirm-go>${escapeHtml(danger)}</button>
      `,
    });

    const go = document.querySelector("[data-confirm-go]");
    if (go) {
      go.addEventListener(
        "click",
        () => {
          form.dataset.confirmed = "true";
          closeModal();
          form.requestSubmit();
        },
        { once: true }
      );
    }
  });

  function escapeHtml(str) {
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  // Optional blocking modal for linked artist deletes (template triggers via button)
  document.addEventListener("click", (e) => {
    const t = e.target;
    if (!(t instanceof Element)) return;
    const btn = t.closest("[data-block-modal]");
    if (!btn) return;
    e.preventDefault();

    const title = btn.getAttribute("data-block-title") || "Cannot delete";
    const message = btn.getAttribute("data-block-message") || "This item cannot be deleted.";
    const link = btn.getAttribute("data-block-link");
    const linkLabel = btn.getAttribute("data-block-link-label") || "View details";

    openModal({
      title,
      body: `<p>${escapeHtml(message)}</p>`,
      footHtml: `
        ${link ? `<a class="btn btn--ghost" href="${link}">${escapeHtml(linkLabel)}</a>` : ""}
        <button class="btn btn--ghost" type="button" data-modal-close>Close</button>
      `,
    });
  });
})();

