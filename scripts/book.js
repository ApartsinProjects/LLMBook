/**
 * Book interactivity: collapsible code blocks and exercise answers.
 * Loaded by all section HTML files via <script defer src="...scripts/book.js">.
 */
document.addEventListener('DOMContentLoaded', function () {

  // 1. Make ALL <pre> code blocks collapsible.
  //    - Caption (.code-caption) and output (.code-output) stay OUTSIDE the <details>
  //    - Short code blocks (10 lines or fewer) start OPEN
  //    - Longer code blocks start COLLAPSED
  document.querySelectorAll('pre').forEach(function (pre) {
    // Skip if already inside a <details> element
    if (pre.closest('details')) return;
    // Skip if inside a callout (exercises, algorithms, etc.)
    if (pre.closest('.callout')) return;
    // Skip inline-style pre (very short, less than 20 chars)
    var text = pre.textContent || '';
    if (text.trim().length < 20) return;

    // Count lines
    var lines = text.split('\n');
    var lineCount = lines.length;
    // Trim trailing empty lines
    while (lineCount > 0 && lines[lineCount - 1].trim() === '') lineCount--;

    var isShort = lineCount <= 10;

    // Create the <details> wrapper
    var details = document.createElement('details');
    details.className = 'code-collapse';
    if (isShort) {
      details.setAttribute('open', '');
    }

    var summary = document.createElement('summary');
    summary.textContent = isShort ? 'Code (' + lineCount + ' lines)' : 'Show Code (' + lineCount + ' lines)';
    details.appendChild(summary);

    // Insert details before the pre, then move pre inside
    pre.parentNode.insertBefore(details, pre);
    details.appendChild(pre);

    // NOTE: .code-output and .code-caption stay OUTSIDE the <details>
    // so they remain visible even when code is collapsed
  });

  // 2. Ensure all exercise <details> are closed by default
  document.querySelectorAll('.callout.exercise details[open]').forEach(function (d) {
    d.removeAttribute('open');
  });

  // 3. Also collapse self-check answers by default (if open)
  document.querySelectorAll('.callout.self-check details[open]').forEach(function (d) {
    d.removeAttribute('open');
  });
});
