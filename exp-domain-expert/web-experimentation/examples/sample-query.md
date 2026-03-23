# Sample Query: web-experimentation

## Question
"How do I set up a redirect test in the Visual Editor?"

## Answer
To create a redirect test (also known as a split URL test) in the Visual Editor:

1. **Create a new experiment** in the Optimizely Web project.
2. **Open the Visual Editor** by clicking "Open in Visual Editor" on the experiment page.
3. **Select a variation** (not the Original) from the variation switcher in the bottom bar.
4. **Add a redirect change:**
   - Click the "Create" menu (or the "+" button) in the bottom bar.
   - Select "Redirect" from the change type options.
   - Enter the destination URL for this variation.
5. **Configure the redirect:**
   - Choose between a simple redirect (full URL) or a regex-based redirect for pattern matching.
   - The Original variation serves as the control and does not redirect.
6. **Set up URL targeting** on the Pages tab to define which pages trigger the experiment.
7. **Save and publish** the experiment.

**Important notes:**
- Redirect tests require the Optimizely snippet to load before the page renders for best results.
- Consider using Performance Edge to eliminate flicker on redirect tests.
- Each variation can redirect to a different URL.
- Query parameters can be preserved or stripped based on configuration.
