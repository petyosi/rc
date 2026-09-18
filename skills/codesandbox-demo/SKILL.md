---
name: codesandbox-demo
description: Create temporary public CodeSandbox browser sandboxes from small frontend examples through the Define API, then verify the rendered preview. Use when the user asks to create, open, or share a CodeSandbox demo. Do not use for CodeSandbox VM SDK or private sandbox management.
---

# CodeSandbox Demo

Create the smallest example that demonstrates the requested behavior. Treat the generated sandbox as public.

## Build the example

- Use a new temporary project directory. Do not submit the repository or working directory wholesale.
- Pin dependency versions. When the user asks for the current npm release, check it before generating `package.json`.
- For small React examples, prefer a Create React App-compatible browser project with `react-scripts@5.0.1`, `public/index.html`, and `src/index.js`. This shape rendered reliably when the Vite/Nodebox preview failed with `Assertion Failed: argument is undefined or null`.
- Use Vite or another runtime only when the example requires it or the user requests it.
- For `@virtuoso.dev/message-list`, wrap the application in `VirtuosoMessageListLicense`. An empty key works on the license-exempt `*.csb.app` preview host. Pin the requested package version.
- Keep styling and interactions sufficient to prove the component works. Avoid unrelated packages and configuration.

## Create the sandbox

Run the included helper:

```bash
node scripts/create-sandbox.mjs <project-directory> [open-file]
```

Resolve `scripts/create-sandbox.mjs` relative to this skill directory. The helper sends the project files as JSON to:

```text
POST https://codesandbox.io/api/v1/sandboxes/define?json=1
```

It requires no CodeSandbox API key. It rejects common secret files, binary files, symlinks, and oversized payloads. Review the exact temporary project contents before submission because the resulting sandbox is accessible by URL.

## Verify

- Open the returned editor URL and wait for dependency installation and the preview.
- Confirm that CodeSandbox reports no build problems.
- Inspect the preview iframe, verify the expected initial content, and exercise the main interaction. For a form example, submit a value and confirm that it appears.
- If the Vite/Nodebox preview shows an internal editor assertion, recreate the project in the React browser shape above instead of repeatedly reloading it.
- If requests show `ERR_BLOCKED_BY_CLIENT`, report the browser extension or content-blocker limitation separately from application errors.
- Keep the working sandbox tab as the deliverable and close failed or duplicate verification tabs.

Return the editor URL. Mention any verification limitation precisely; do not claim an interaction passed unless it was observed.
