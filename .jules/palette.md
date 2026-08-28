## 2024-05-24 - Interactive Div Accessibility
**Learning:** Custom interactive elements (like custom div dropzones) that rely solely on `click` listeners and `cursor-pointer` classes are inaccessible to keyboard users, which forms a pattern across UI components. They miss focus rings and keyboard triggers.
**Action:** Always ensure interactive non-button elements have `role="button"`, `tabindex="0"`, focus indicators (e.g., `focus-visible:ring`), and `keydown` event listeners for `Enter` and `Space` keys to mimic native button behavior.

## 2024-05-24 - Modal Close Buttons Accessibility
**Learning:** Icon-only modal close buttons often lack `aria-label`s, focus styles, and have screen reader readable icons which degrades keyboard navigation and screen reader experience.
**Action:** When adding or reviewing modals, ensure that close buttons always include an `aria-label` (e.g., `aria-label="Close"`), proper keyboard focus styling (`focus-visible:ring-2`), and that inner icon elements have `aria-hidden="true"`.
