document.addEventListener("DOMContentLoaded", function() {
    
    /*
     * ROW COLLAPSES
     */

    document.body.addEventListener('tree-grid:toggle-all', (e) => {
        const tree = e.target.closest('.tree-grid');
        if (!tree) {
            return;
        }
        const doOpen = e.detail.doOpen;
        Array.from(tree.querySelectorAll('.tree-row[aria-level]')).map((row) => {
            if (doOpen === true || (doOpen !== false && !treeRowIsOpen(row))) {
                openTreeRow(row);
            }
            else {
                collapseTreeRow(row);
            }
        });
    });

    document.body.addEventListener('tree-grid:toggle', (e) => {
        const row = e.target.closest('.tree-row[aria-level]');
        if (!row) {
            return;
        }
        const doOpen = e.detail.doOpen;
        if (doOpen === true || (doOpen !== false && !treeRowIsOpen(row))) {
            openTreeRow(row, e.detail.skipChildren);
        }
        else {
            collapseTreeRow(row);
        }
    });

    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('.tree-row-collapse');
        if (!btn) {
            return;
        }
        e.preventDefault();

        const row = btn.closest('.tree-row');
        const tree = row.closest('.tree-grid');

        if (treeRowIsOpen(row)) {
            collapseTreeRow(row);
        }
        else {
            openTreeRow(row);
        }
    });

    function treeRowIsOpen(row) {
        return row.querySelector('.fa-angle-down') != null;
    }

    function treeRowLevel(row) {
        return parseInt(row.getAttribute('aria-level'));
    }

    function collapseTreeRow(row) {
        const level = treeRowLevel(row);
        const children = nextUntil(row, `.tree-row[aria-level="${level}"]`).filter(childRow => treeRowLevel(childRow) > level);
        children.map((childRow) => {
            collapseTreeRow(childRow);
            childRow.hidden = true;
        });
        toggleCollapseIcon(row, 'collapse');
    }

    function openTreeRow(row, skipChildren) {
        const level = treeRowLevel(row);

        if (skipChildren !== true) {
            const children = nextUntil(row, `.tree-row[aria-level="${level}"]`).filter(childRow => treeRowLevel(childRow) == level + 1);
            children.map((childRow) => {
                childRow.hidden = false;
            });
        }

        toggleCollapseIcon(row, 'open');

        const parent = prevAll(row, `.tree-row[aria-level="${level - 1}"]`)[0];
        if (parent) {
            if (skipChildren) {
                row.hidden = false; // won't be opened by its parent
            }
            openTreeRow(parent, skipChildren);
        }
    }

    function toggleCollapseIcon(buttons, direction) {
        if (buttons == undefined) {
            return;
        }
        if (!Array.isArray(buttons)) {
            buttons = [buttons];
        }
        for (const button of buttons) {
            const icons = Array.from(button.querySelectorAll('i.fa-angle-down, i.fa-angle-right'));
            if (direction === 'open') {
                icons.map(x => x.classList.add('fa-angle-down') || x.classList.remove('fa-angle-right'));
            }
            else if (direction === 'collapse') {
                icons.map(x => x.classList.add('fa-angle-right') || x.classList.remove('fa-angle-down'));
            }
            else {
                icons.map(x => x.classList.toggle('fa-angle-right') || x.classList.toggle('fa-angle-down'));
            }
        }
    }

    /*
     * UTILITIES
     */

    function nextUntil(elem, selector) {
        const siblings = [];
        let next = elem.nextElementSibling;
        while (next) {
            if (selector && next.matches(selector)) {
            break;
            }
            siblings.push(next);
            next = next.nextElementSibling;
        }
        return siblings;
    }

    function prevAll(elem, selector) {
        const siblings = [];
        let prev = elem.previousElementSibling;
        while (prev) {
            if (!selector || prev.matches(selector)) {
                siblings.push(prev);
            }
            prev = prev.previousElementSibling;
        }
        return siblings;
    }
});