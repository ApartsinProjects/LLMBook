/**
 * Book interactivity: collapsible code blocks, exercises, and answers.
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

  // 2. Remove standalone "Exercises" headings (redundant with the container title).
  //    Matches <h2>Exercises</h2> that directly precede exercise callouts.
  document.querySelectorAll('h2').forEach(function (h2) {
    if (h2.textContent.trim() === 'Exercises') {
      // Check if the next meaningful sibling is an exercise callout
      var next = h2.nextElementSibling;
      while (next && next.nodeType === 1 && next.tagName === 'BR') next = next.nextElementSibling;
      if (next && next.classList.contains('callout') && next.classList.contains('exercise')) {
        h2.remove();
      }
    }
  });

  // 3. Merge consecutive exercise callouts into a single collapsible container.
  //    Finds runs of adjacent .callout.exercise elements and wraps them in one
  //    <details> block, collapsed by default.
  var exercises = document.querySelectorAll('.callout.exercise');
  var processed = new Set();

  exercises.forEach(function (ex) {
    if (processed.has(ex)) return;

    // Collect the run of consecutive .callout.exercise siblings
    var group = [ex];
    processed.add(ex);
    var next = ex.nextElementSibling;
    while (next && next.classList.contains('callout') && next.classList.contains('exercise')) {
      group.push(next);
      processed.add(next);
      next = next.nextElementSibling;
    }

    // Count exercises in this group
    var count = group.length;

    // Create wrapper <details> (collapsed by default)
    var wrapper = document.createElement('details');
    wrapper.className = 'exercises-container';

    var summary = document.createElement('summary');
    summary.className = 'exercises-summary';
    summary.innerHTML = '<span class="exercises-icon">&#9998;</span> Exercises (' + count + ')';
    wrapper.appendChild(summary);

    // Insert wrapper before the first exercise
    group[0].parentNode.insertBefore(wrapper, group[0]);

    // Move all exercises into the wrapper
    group.forEach(function (el) {
      // Remove the outer callout border since the wrapper provides it
      el.classList.add('exercise-inside-group');
      // Ensure individual exercise answers are collapsed
      el.querySelectorAll('details[open]').forEach(function (d) {
        d.removeAttribute('open');
      });
      wrapper.appendChild(el);
    });
  });

  // 3. Also collapse self-check answers by default (if open)
  document.querySelectorAll('.callout.self-check details[open]').forEach(function (d) {
    d.removeAttribute('open');
  });
});
