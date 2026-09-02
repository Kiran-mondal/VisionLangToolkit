## 2024-05-24 - Interactive Div Accessibility
**Learning:** Custom interactive elements (like custom div dropzones) that rely solely on `click` listeners and `cursor-pointer` classes are inaccessible to keyboard users, which forms a pattern across UI components. They miss focus rings and keyboard triggers.
**Action:** Always ensure interactive non-button elements have `role="button"`, `tabindex="0"`, focus indicators (e.g., `focus-visible:ring`), and `keydown` event listeners for `Enter` and `Space` keys to mimic native button behavior.

## 2024-05-24 - Modal Close Buttons Accessibility
**Learning:** Icon-only modal close buttons often lack `aria-label`s, focus styles, and have screen reader readable icons which degrades keyboard navigation and screen reader experience.
**Action:** When adding or reviewing modals, ensure that close buttons always include an `aria-label` (e.g., `aria-label="Close"`), proper keyboard focus styling (`focus-visible:ring-2`), and that inner icon elements have `aria-hidden="true"`.

## 2024-05-24 - Form Label Accessibility
**Learning:** Using heading elements (`<h4>`) instead of `<label>` tags for form inputs breaks screen reader association, making forms inaccessible to users relying on assistive technologies.
**Action:** Always use `<label>` tags with a `for` attribute that matches the corresponding input's `id` to ensure proper accessibility and screen reader support for all form fields.

## 2024-05-24 - Custom Toggle Button Accessibility
**Learning:** Custom UI toggle buttons (like dark mode switches) built with standard `<button>` elements and CSS transforms often lack semantic meaning, causing screen readers to announce them as generic buttons without indicating their on/off state to visually impaired users.
**Action:** When implementing custom toggles, always add `role="switch"` and an `aria-checked` attribute that dynamically updates between `"true"` and `"false"` via JavaScript to communicate the current state to assistive technologies.

## 2024-05-18 - [Interactive Image Accessibility]
**Learning:** Found an `<img>` tag used as an interactive element (`profileBtn`) that triggered a modal onClick. While visually it works, it completely bypasses keyboard accessibility because `<img>` tags aren't natively focusable and don't receive Enter/Space key events.
**Action:** When creating clickable avatar/profile icons that trigger actions, wrap the `<img>` inside a `<button>` element. Move the ID and click handlers to the `<button>`, apply `focus-visible` styles to the `<button>`, and add an `aria-label` to the button while leaving the inner `<img>` `alt` text empty (`alt=""`) to avoid redundant screen reader announcements.
