# Sample Output: read-jira-context

### Ticket Details
- **Key:** CJS-10873
- **Summary:** Add thread_id to Segment tracking events
- **Type:** Story
- **Status:** In Review
- **Priority:** Normal
- **Assignee:** John Doe
- **Reporter:** Jane Smith
- **Labels:** Requires_QA, Tracking
- **Components:** Web

### Description & Acceptance Criteria
As a user, I want thread_id included in all Segment tracking events so that we can correlate user actions within a session.

AC:
1. Add thread_id property to all experiment-related Segment events
2. thread_id should persist across the user session
3. Ensure backward compatibility with existing event consumers

### Relevant Comments (2)
- **Author:** Jane Smith | **Date:** 2024-01-15
- **Content:** thread_id should be generated on experiment creation, not page load

- **Author:** Dev Lead | **Date:** 2024-01-16
- **Content:** We'll store thread_id in the experiment store, similar to how we handle session_id

### Linked Tickets (1)
- **CJS-10870:** Refactor Segment event properties | Link type: Relates to | Status: Merged

### Epic Context
- **Epic Key:** CJS-10800
- **Epic Summary:** Segment Tracking Improvements Q1
- **Children:** 8 total, 2 with Requires_QA, 1 bug

### URLs Found
- **Confluence:** https://optimizely-ext.atlassian.net/wiki/spaces/EXPENG/pages/12345/Tracking+Spec
- **Figma:** (none)
- **Other:** (none)
